 document.addEventListener('DOMContentLoaded', function () {
               const form = document.getElementById('registerForm');
               const usernameInput = document.getElementById('username');
               const emailInput = document.getElementById('email');
               const passwordInput = document.getElementById('password');
               const confirmPasswordInput = document.getElementById('confirm_password');

               const usernameError = document.getElementById('usernameError');
               const emailError = document.getElementById('emailError');
               const passwordError = document.getElementById('passwordError');
               const confirmPasswordError = document.getElementById('confirmPasswordError');

               const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
               const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/
;

               let confirmPasswordTouched = false;

               // Username real-time validation
               usernameInput.addEventListener('input', function () {
                   if (!usernameInput.value.trim()) {
                       usernameError.textContent = 'Username is required';
                       usernameInput.classList.add('is-invalid');
                   } else {
                       usernameError.textContent = '';
                       usernameInput.classList.remove('is-invalid');
                   }
               });

               // Real-time validation for password
               passwordInput.addEventListener('input', function () {
                   if (!passwordRegex.test(passwordInput.value)) {
                       passwordError.textContent = 'Password must be 8+ characters with uppercase, lowercase, number, and special character';
                       passwordInput.classList.add('is-invalid');
                   } else {
                       passwordError.textContent = '';
                       passwordInput.classList.remove('is-invalid');
                   }

                   // Only validate confirm password if user already interacted with it
                   if (confirmPasswordTouched) {
                       validateConfirmPassword();
                   }
               });

               // Detect when user types in confirm password field
               confirmPasswordInput.addEventListener('input', function () {
                   confirmPasswordTouched = true;
                   validateConfirmPassword();
               });

               // Validate confirm password
               function validateConfirmPassword() {
                   if (passwordInput.value !== confirmPasswordInput.value) {
                       confirmPasswordError.textContent = 'Passwords do not match';
                       confirmPasswordInput.classList.add('is-invalid');
                   } else {
                       confirmPasswordError.textContent = '';
                       confirmPasswordInput.classList.remove('is-invalid');
                   }
               }

               // Real-time email validation
               emailInput.addEventListener('input', function () {
                   if (!emailRegex.test(emailInput.value)) {
                       emailError.textContent = 'Enter a valid email';
                       emailInput.classList.add('is-invalid');
                   } else {
                       emailError.textContent = '';
                       emailInput.classList.remove('is-invalid');
                   }
               });

               // On form submit
               form.addEventListener('submit', function (event) {
                   event.preventDefault();
                   let isValid = true;

                   // Username validation
                   if (!usernameInput.value.trim()) {
                       usernameError.textContent = 'Username is required';
                       usernameInput.classList.add('is-invalid');
                       isValid = false;
                   } else {
                       usernameError.textContent = '';
                       usernameInput.classList.remove('is-invalid');
                   }

                   // Email validation
                   if (!emailRegex.test(emailInput.value)) {
                       emailError.textContent = 'Enter a valid email';
                       emailInput.classList.add('is-invalid');
                       isValid = false;
                   } else {
                       emailError.textContent = '';
                       emailInput.classList.remove('is-invalid');
                   }

                   // Password validation
                   if (!passwordRegex.test(passwordInput.value)) {
                       passwordError.textContent = 'Password must be 8+ characters with uppercase, lowercase, number, and special character';
                       passwordInput.classList.add('is-invalid');
                       isValid = false;
                   } else {
                       passwordError.textContent = '';
                       passwordInput.classList.remove('is-invalid');
                   }

                   // Confirm password validation
                   if (passwordInput.value !== confirmPasswordInput.value) {
                       confirmPasswordError.textContent = 'Passwords do not match';
                       confirmPasswordInput.classList.add('is-invalid');
                       isValid = false;
                   } else {
                       confirmPasswordError.textContent = '';
                       confirmPasswordInput.classList.remove('is-invalid');
                   }

                   if (isValid) {
                       form.submit();
                   }
               });
           });