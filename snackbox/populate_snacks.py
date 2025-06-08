import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snackbox.settings')
django.setup()

from core.models import Snack

# Clear existing snacks
Snack.objects.all().delete()

# Define snacks with categories
snacks_data = [
    Snack(name="Chia Seed Pudding", description="A creamy pudding made with chia seeds and coconut milk", price=4.50, is_vegan=True, is_gluten_free=True, is_nut_free=False, stock=40, category='specialty'),
    Snack(name="Quinoa Energy Bars", description="Chewy bars packed with quinoa, seeds, and dried fruit", price=3.99, is_vegan=True, is_gluten_free=True, is_nut_free=False, stock=60, category='bars_bites'),
    Snack(name="Nut-Free Granola Bites", description="Bite-sized granola clusters, safe for nut allergies", price=5.25, is_vegan=False, is_gluten_free=False, is_nut_free=True, stock=30, category='bars_bites'),
    Snack(name="Roasted Chickpea Snacks", description="Crispy roasted chickpeas with a savory seasoning", price=2.99, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=80, category='roasted_spiced'),
    Snack(name="Coconut Macaroons", description="Soft coconut macaroons, lightly sweetened", price=4.75, is_vegan=False, is_gluten_free=True, is_nut_free=True, stock=25, category='cookies_sweets'),
    Snack(name="Dark Chocolate Sea Salt Bars", description="Dark chocolate bars with a hint of sea salt", price=3.50, is_vegan=True, is_gluten_free=True, is_nut_free=False, stock=50, category='bars_bites'),
    Snack(name="Pumpkin Seed Clusters", description="Crunchy clusters of pumpkin seeds and honey", price=4.20, is_vegan=False, is_gluten_free=True, is_nut_free=True, stock=35, category='crackers_clusters'),
    Snack(name="Vegan Protein Balls", description="Protein-packed balls made with pea protein and dates", price=5.99, is_vegan=True, is_gluten_free=False, is_nut_free=False, stock=45, category='bars_bites'),
    Snack(name="Rice Cakes with Avocado", description="Mini rice cakes topped with avocado spread", price=3.25, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=70, category='chips_crisps'),
    Snack(name="Dried Mango Slices", description="Sweet and tangy dried mango slices", price=4.00, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=55, category='dried_fruits'),
    Snack(name="Oatmeal Energy Cookies", description="Soft oatmeal cookies with raisins and cinnamon", price=4.80, is_vegan=False, is_gluten_free=False, is_nut_free=True, stock=40, category='cookies_sweets'),
    Snack(name="Kale Chips", description="Crispy baked kale chips with a touch of salt", price=3.75, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=60, category='chips_crisps'),
    Snack(name="Peanut Butter Protein Bars", description="Protein bars with a creamy peanut butter layer", price=5.50, is_vegan=False, is_gluten_free=True, is_nut_free=False, stock=30, category='bars_bites'),
    Snack(name="Apple Cinnamon Crisps", description="Baked apple slices with a hint of cinnamon", price=3.99, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=65, category='chips_crisps'),
    Snack(name="Mixed Seed Crackers", description="Crackers made with a blend of seeds", price=4.25, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=50, category='crackers_clusters'),
    Snack(name="Banana Chips", description="Crispy banana chips, naturally sweet", price=2.50, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=90, category='chips_crisps'),
    Snack(name="Almond Butter Energy Bites", description="Energy bites with almond butter and oats", price=5.75, is_vegan=True, is_gluten_free=True, is_nut_free=False, stock=35, category='bars_bites'),
    Snack(name="Sunflower Seed Bars", description="Bars made with sunflower seeds and maple syrup", price=4.10, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=55, category='bars_bites'),
    Snack(name="Cashew Clusters", description="Clusters of cashews with a caramel coating", price=4.90, is_vegan=True, is_gluten_free=True, is_nut_free=False, stock=40, category='crackers_clusters'),
    Snack(name="Vegan Brownie Bites", description="Rich chocolate brownie bites, vegan-friendly", price=5.20, is_vegan=True, is_gluten_free=True, is_nut_free=False, stock=50, category='bars_bites'),
    Snack(name="Popped Sorghum Snacks", description="Light and crunchy popped sorghum", price=3.00, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=75, category='popcorn_puffs'),
    Snack(name="Cinnamon Roasted Peas", description="Roasted peas with a cinnamon twist", price=3.40, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=60, category='roasted_spiced'),
    Snack(name="Flaxseed Crackers", description="Crisp crackers made with flaxseeds", price=4.00, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=45, category='crackers_clusters'),
    Snack(name="Date and Coconut Balls", description="Sweet balls made with dates and coconut", price=4.60, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=50, category='dried_fruits'),
    Snack(name="Spiced Edamame Snacks", description="Spicy roasted edamame for a healthy snack", price=3.80, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=65, category='roasted_spiced'),
    Snack(name="Gluten-Free Pretzels", description="Classic pretzels, gluten-free", price=3.50, is_vegan=False, is_gluten_free=True, is_nut_free=True, stock=70, category='specialty'),
    Snack(name="Maple Pumpkin Seed Bars", description="Bars with pumpkin seeds and maple flavor", price=4.30, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=40, category='bars_bites'),
    Snack(name="Cranberry Seed Clusters", description="Clusters with cranberries and seeds", price=4.70, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=55, category='crackers_clusters'),
    Snack(name="Seaweed Snacks", description="Lightly salted seaweed snacks", price=2.80, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=80, category='specialty'),
    Snack(name="Vegan Cheese Puffs", description="Cheesy puffs made with vegan cheese", price=3.90, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=60, category='popcorn_puffs'),
    Snack(name="Pistachio Energy Bars", description="Energy bars with pistachios and dates", price=5.00, is_vegan=True, is_gluten_free=True, is_nut_free=False, stock=35, category='bars_bites'),
    Snack(name="Dried Apricot Slices", description="Sweet dried apricots, perfect for snacking", price=4.20, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=50, category='dried_fruits'),
    Snack(name="Hemp Seed Granola", description="Granola with hemp seeds and oats", price=4.80, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=45, category='bars_bites'),
    Snack(name="Chocolate-Dipped Rice Cakes", description="Rice cakes dipped in dark chocolate", price=4.50, is_vegan=False, is_gluten_free=True, is_nut_free=True, stock=40, category='chips_crisps'),
    Snack(name="Spicy Chickpea Chips", description="Crispy chickpea chips with a spicy kick", price=3.60, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=70, category='roasted_spiced'),
    Snack(name="Blueberry Oat Bars", description="Oat bars with dried blueberries", price=4.40, is_vegan=False, is_gluten_free=False, is_nut_free=True, stock=55, category='bars_bites'),
    Snack(name="Vegan Caramel Popcorn", description="Popcorn with a vegan caramel coating", price=3.20, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=65, category='popcorn_puffs'),
    Snack(name="Sesame Seed Sticks", description="Crunchy sticks made with sesame seeds", price=3.10, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=60, category='crackers_clusters'),
    Snack(name="Matcha Energy Balls", description="Energy balls with a matcha green tea flavor", price=5.30, is_vegan=True, is_gluten_free=True, is_nut_free=False, stock=40, category='bars_bites'),
    Snack(name="Zucchini Chips", description="Baked zucchini chips with sea salt", price=3.70, is_vegan=True, is_gluten_free=True, is_nut_free=True, stock=50, category='chips_crisps'),
]

# Bulk create snacks
Snack.objects.bulk_create(snacks_data)

print(f"Successfully added {len(snacks_data)} snacks to the database!")