# core/views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db import IntegrityError
import re
from django.http import JsonResponse, Http404
from .models import *
from django.http import HttpResponseRedirect
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from collections import defaultdict
import json
from django.db.models import Q

def home(request):
    user_id = request.COOKIES.get('user_id')
    snacks = Snack.objects.all()
    filtered_snacks = snacks

    # Group snacks by category and store total counts
    category_data = defaultdict(lambda: {'snacks': [], 'total_count': 0})
    
    for snack in filtered_snacks:
        category = snack.get_category_display()
        category_data[category]['snacks'].append(snack)
        category_data[category]['total_count'] += 1

    # Limit snacks per category to 4
    for category in category_data:
        category_data[category]['snacks'] = category_data[category]['snacks'][:6]

    # Sort categories by total count descending
    sorted_categories = dict(
        sorted(category_data.items(), key=lambda item: item[1]['total_count'], reverse=True)
    )

    # Calculate cart items count for navbar
    cart_items_count = 0
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            cart, created = Cart.objects.get_or_create(user=user)
            cart_items_count = cart.cartitem_set.count()
        except User.DoesNotExist:
            pass

    # Get query parameters to pass to the template
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'name_asc')
    category = request.GET.get('category', '')
    is_vegan = 'is_vegan' in request.GET
    is_gluten_free = 'is_gluten_free' in request.GET
    is_nut_free = 'is_nut_free' in request.GET

    return render(request, 'core/home.html', {
        'categories': sorted_categories,
        'category_choices': Snack.CATEGORY_CHOICES,
        'cart_items_count': cart_items_count,
        'query': query,
        'sort_by': sort_by,
        'category': category,
        'is_vegan': is_vegan,
        'is_gluten_free': is_gluten_free,
        'is_nut_free': is_nut_free,
    })

# The rest of the views.py file remains unchanged
def category_detail(request, category_slug):
    # Map the slug back to the category display name
    category_map = {slug: display for slug, display in Snack.CATEGORY_CHOICES}
    reverse_category_map = {display.lower().replace(' & ', '-').replace(' ', '-'): display for slug, display in Snack.CATEGORY_CHOICES}

    # Normalize the category_slug by replacing underscores with hyphens
    normalized_slug = category_slug.replace('_', '-')

    # Try exact match first
    category_name = reverse_category_map.get(normalized_slug)

    # If exact match fails, try partial match and redirect
    if not category_name:
        for slug, display in reverse_category_map.items():
            if normalized_slug == slug.split('-')[0]:
                return redirect('category_detail', category_slug=slug)
        raise Http404(f"The category '{category_slug.replace('-', ' ').title()}' does not exist.")

    # Find the corresponding category slug for the display name
    category_slugs = [slug for slug, display in Snack.CATEGORY_CHOICES if display == category_name]
    snacks = Snack.objects.filter(category__in=category_slugs)

    # Get query parameters
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'name_asc')
    is_vegan = 'is_vegan' in request.GET
    is_gluten_free = 'is_gluten_free' in request.GET
    is_nut_free = 'is_nut_free' in request.GET

    # Apply search query
    if query:
        snacks = snacks.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Apply manual dietary filters
    if is_vegan:
        snacks = snacks.filter(is_vegan=True)
    if is_gluten_free:
        snacks = snacks.filter(is_gluten_free=True)
    if is_nut_free:
        snacks = snacks.filter(is_nut_free=True)

    # Apply sorting
    if sort_by == 'name_asc':
        snacks = snacks.order_by('name')
    elif sort_by == 'name_desc':
        snacks = snacks.order_by('-name')
    elif sort_by == 'price_asc':
        snacks = snacks.order_by('price')
    elif sort_by == 'price_desc':
        snacks = snacks.order_by('-price')

    # Calculate cart items count for navbar
    cart_items_count = 0
    user_id = request.COOKIES.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            cart, created = Cart.objects.get_or_create(user=user)
            cart_items_count = cart.cartitem_set.count()
        except User.DoesNotExist:
            pass

    # Find the corresponding category slug for the display name
    category_slug_value = next(slug for slug, display in Snack.CATEGORY_CHOICES if display == category_name)

    return render(request, 'core/category_detail.html', {
        'category': category_name,
        'snacks': snacks,
        'cart_items_count': cart_items_count,
        'categories': Snack.CATEGORY_CHOICES,
        'category_slug': category_slug_value,
        'query': query,
        'sort_by': sort_by,
        'is_vegan': is_vegan,
        'is_gluten_free': is_gluten_free,
        'is_nut_free': is_nut_free,
    })

def cart(request):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=user)
    cart_items_count = cart.cartitem_set.count()

    return render(request, 'core/cart.html', {
        'cart': cart,
        'cart_items_count': cart_items_count
    })

def checkout(request):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=user)
    cart_items_count = cart.cartitem_set.count()

    return render(request, 'core/checkout.html', {
        'cart': cart,
        'cart_items_count': cart_items_count,
        'user': user
    })

def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return JsonResponse({
            'status': 'error',
            'message': 'Please log in to add items to cart',
            'redirect': '/login/'  # <-- add redirect URL here
        }, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    data = json.loads(request.body)
    snack_id = data.get('snack_id')
    quantity_change = int(data.get('quantity', 1))

    try:
        snack = Snack.objects.get(id=snack_id)
    except Snack.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Snack not found'}, status=404)

    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, snack=snack)

    new_quantity = cart_item.quantity + quantity_change

    if new_quantity > snack.stock:
        return JsonResponse({'status': 'error', 'message': 'Not enough stock available'}, status=400)

    if new_quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = new_quantity
        cart_item.save()

    return JsonResponse({'status': 'success', 'message': 'Cart updated'})


def update_cart(request, item_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Please log in'}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=user)
    except CartItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cart item not found'}, status=404)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        cart_item.delete()
        return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
    else:
        if cart_item.snack.stock < quantity:
            return JsonResponse({'status': 'error', 'message': 'Not enough stock available'}, status=400)
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'status': 'success', 'message': 'Cart updated'})

def remove_from_cart(request, item_id):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=user)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def process_payment(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Please log in'}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', "message": 'User not found'}, status=404)

    cart, created = Cart.objects.get_or_create(user=user)
    if not cart.cartitem_set.exists():
        return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)

    # Create the order
    total_amount = cart.total_price
    order = Order.objects.create(
        user=user,
        total_amount=total_amount,
        status='COMPLETED'
    )

    # Create order items
    for cart_item in cart.cartitem_set.all():
        OrderItem.objects.create(
            order=order,
            snack=cart_item.snack,
            quantity=cart_item.quantity,
            price=cart_item.snack.price
        )
        # Update stock
        cart_item.snack.stock -= cart_item.quantity
        cart_item.snack.save()

    # Clear the cart
    cart.cartitem_set.all().delete()

    return JsonResponse({'status': 'success', 'message': 'Order placed successfully', 'order_id': order.id})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name', '')
        is_vegan = request.POST.get('is_vegan') == 'on'
        is_gluten_free = request.POST.get('is_gluten_free') == 'on'
        is_nut_free = request.POST.get('is_nut_free') == 'on'

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            # Create a UserProfile for the new user
            UserProfile.objects.create(
                user=user,
                full_name=full_name,
                is_vegan=is_vegan,
                is_gluten_free=is_gluten_free,
                is_nut_free=is_nut_free
            )
            return redirect('login')
        except IntegrityError:
            return render(request, 'core/register.html', {'error': 'Username already exists'})

    return render(request, 'core/register.html')

def login(request):
    if request.method=='POST':
        email=request.POST.get('email','').strip()
        password=request.POST.get('password','').strip()

        errors={}

        # Email validation 
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not email :
            errors['email']='Email is required'
        elif not re.match(email_regex,email):
            errors['email']='Enter a valid email address'

        # Password validation 
        if not password :
            errors['password']='Password is required'

        if errors :
            return render(request, 'core/login.html',{
                'errors':errors,
                'email':email
            })
        
        #checking if user exists 
        user=User.objects.filter(email=email).first()
        if not user :
            errors['general']='Invalid Email or Password'
            return render(request, 'core/login.html',{
                'errors':errors,
                'email':email
            })
        #Verify the password 
        if not user.check_password(password) :
            errors['general']='Invalid Email or Password'
            return render(request, 'core/login.html',{
                'errors':errors,
                'email':email
            })
        
         # If authentication is successful, return user ID
        return JsonResponse({'status':'success','user_id':user.id})
     
    return render(request,'core/login.html')

def logout(request):
    response = redirect('home')
    response.set_cookie('user_id', '', max_age=0)
    return response

def profile(request):
    # Check if the user is logged in by looking for the user_id cookie
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return redirect('login')
    
    # Fetch the user from the database
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')
    
    # Get or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Calculate cart items count for navbar
    cart_items_count = 0
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items_count = cart.cartitem_set.count()

    # Handle form submission (POST request)
    if request.method == 'POST':
        # Update all profile fields with the form data
        profile.full_name = request.POST.get('full_name', '')
        profile.phone_number = request.POST.get('phone_number', '')
        profile.street = request.POST.get('street', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.country = request.POST.get('country', '')
        # Checkboxes for dietary preferences (still allow saving preferences, but they won't affect filtering)
        profile.is_vegan = 'is_vegan' in request.POST
        profile.is_gluten_free = 'is_gluten_free' in request.POST
        profile.is_nut_free = 'is_nut_free' in request.POST
        # Save the updated profile to the database
        profile.save()
        # Redirect to the same page to show the updated profile
        return redirect('profile')

    return render(request, 'core/profile.html', {
        'profile': profile,
        'cart_items_count': cart_items_count
    })

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

        if not email:
            return render(request, 'core/forgot_password.html', {
                'message': 'Email is required',
                'message_type': 'error'
            })
        if not re.match(email_regex, email):
            return render(request, 'core/forgot_password.html', {
                'message': 'Enter a valid email address',
                'message_type': 'error'
            })

        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, 'core/forgot_password.html', {
                'message': 'No account found with this email',
                'message_type': 'error'
            })

        # Generate a password reset token
        token = PasswordResetToken(
            user=user,
            expires_at=timezone.now() + timedelta(hours=1)  # Token expires in 1 hour
        )
        token.save()

        # Send the reset link via email
        reset_url = f"http://localhost:8000/reset-password/{token.token}/"
        try:
            send_mail(
                subject='Password Reset Request - SnackBox',
                message=f'Click the link to reset your password: {reset_url}',
                from_email=None,  # Will use DEFAULT_FROM_EMAIL from settings
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
            return render(request, 'core/forgot_password.html', {
                'message': 'Failed to send email. Please try again later.',
                'message_type': 'error'
            })

        return render(request, 'core/forgot_password.html', {
            'message': 'A password reset link has been sent to your email.',
            'message_type': 'success'
        })

    return render(request, 'core/forgot_password.html')

def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return render(request, 'core/reset_password.html', {
            'message': 'Invalid or expired token',
            'message_type': 'error'
        })

    if timezone.now() > reset_token.expires_at:
        reset_token.delete()
        return render(request, 'core/reset_password.html', {
            'message': 'This token has expired',
            'message_type': 'error'
        })

    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'

        if not password:
            return render(request, 'core/reset_password.html', {
                'message': 'Password is required',
                'message_type': 'error'
            })
        if not re.match(password_regex, password):
            return render(request, 'core/reset_password.html', {
                'message': 'Password must be 8+ characters with uppercase, lowercase, number, and special character',
                'message_type': 'error'
            })
        if password != confirm_password:
            return render(request, 'core/reset_password.html', {
                'message': 'Passwords do not match',
                'message_type': 'error'
            })

        user = reset_token.user
        user.set_password(password)
        user.save()

        reset_token.delete()

        return render(request, 'core/reset_password.html', {
            'message': 'Password reset successfully. You can now log in with your new password.',
            'message_type': 'success'
        })

    return render(request, 'core/reset_password.html')

def search_results(request):
    # Get query parameters
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'name_asc')
    category = request.GET.get('category', '')
    is_vegan = 'is_vegan' in request.GET
    is_gluten_free = 'is_gluten_free' in request.GET
    is_nut_free = 'is_nut_free' in request.GET

    # Start with all snacks
    snacks = Snack.objects.all()

    # Apply category filter
    if category:
        snacks = snacks.filter(category=category)

    # Apply search query
    if query:
        snacks = snacks.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Apply manual dietary filters
    if is_vegan:
        snacks = snacks.filter(is_vegan=True)
    if is_gluten_free:
        snacks = snacks.filter(is_gluten_free=True)
    if is_nut_free:
        snacks = snacks.filter(is_nut_free=True)

    # Apply sorting
    if sort_by == 'name_asc':
        snacks = snacks.order_by('name')
    elif sort_by == 'name_desc':
        snacks = snacks.order_by('-name')
    elif sort_by == 'price_asc':
        snacks = snacks.order_by('price')
    elif sort_by == 'price_desc':
        snacks = snacks.order_by('-price')

    # Calculate cart items count for navbar
    cart_items_count = 0
    user_id = request.COOKIES.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            cart, created = Cart.objects.get_or_create(user=user)
            cart_items_count = cart.cartitem_set.count()
        except User.DoesNotExist:
            pass

    # Prepare context for the template
    context = {
        'snacks': snacks,
        'cart_items_count': cart_items_count,
        'query': query,
        'sort_by': sort_by,
        'category': category,
        'is_vegan': is_vegan,
        'is_gluten_free': is_gluten_free,
        'is_nut_free': is_nut_free,
        'categories': Snack.CATEGORY_CHOICES,
    }

    return render(request, 'core/search_results.html', context)

def contact_us(request):
    if request.method == 'POST':
        pass
    return render(request, 'core/contact_us.html')

def about_us(request):
    return render(request, 'core/about_us.html')