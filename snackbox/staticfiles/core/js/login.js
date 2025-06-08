document.getElementById('loginForm').addEventListener('submit', function(event) {
       event.preventDefault(); // Prevent default form submission

       const form = this;
       const formData = new FormData(form);
       const generalError = document.getElementById('generalError');
       const emailInput = document.getElementById('email');
       const passwordInput = document.getElementById('password');
       const emailError = document.getElementById('emailError');
       const passwordError = document.getElementById('passwordError');
       const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

       // Log the CSRF token to verify it's being retrieved
       console.log('CSRF Token:', csrfToken);

       // Clear previous errors
       generalError.classList.add('d-none');
       emailError.textContent = '';
       passwordError.textContent = '';
       emailInput.classList.remove('is-invalid');
       passwordInput.classList.remove('is-invalid');

       fetch('/login/', {
         method: 'POST',
         body: formData,
         headers: {
           'X-CSRFToken': csrfToken
         }
       })
       .then(response => {
         // Log the response status for debugging
         console.log('Response Status:', response.status);
         if (!response.ok) {
           throw new Error(`HTTP error! Status: ${response.status}`);
         }
         return response.json();
       })
       .then(data => {
         console.log('Response Data:', data);
         if (data.status === 'success') {
           // Set the cookie client-side
           document.cookie = `user_id=${data.user_id}; max-age=3600; path=/`;
           // Redirect to home page
           window.location.href = '/';
         } else {
           // Display errors
           if (data.errors.general) {
             generalError.textContent = data.errors.general;
             generalError.classList.remove('d-none');
           }
           if (data.errors.email) {
             emailError.textContent = data.errors.email;
             emailInput.classList.add('is-invalid');
           }
           if (data.errors.password) {
             passwordError.textContent = data.errors.password;
             passwordInput.classList.add('is-invalid');
           }
         }
       })
       .catch(error => {
         console.error('Error:', error);
         generalError.textContent = 'An error occurred. Please try again.';
         generalError.classList.remove('d-none');
       });
     });