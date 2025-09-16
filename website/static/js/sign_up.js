// SIGNUP FORM VALIDATION
document.addEventListener("DOMContentLoaded", function () {
  const signupform = document.getElementById('signup-form');
  if (!signupform) return;  // Only run on signup page

  const firstname_input = document.getElementById('firstName');
  const email_input = document.getElementById('email');
  const password_input = document.getElementById('password1');
  const re_enter_password_input = document.getElementById('password2');
  const error_message = document.getElementById('error-message');
  const success_message = document.getElementById('success-message');

  signupform.addEventListener('submit', (e) => {
    let errors = getSignupFormErrors(
      firstname_input.value.trim(),
      email_input.value.trim(),
      password_input.value,
      re_enter_password_input.value
    );

    if (errors.length > 0) {
      e.preventDefault();
      error_message.innerHTML = errors.join('<br>');
      success_message.innerText = '';
    } else {
   
    }
  });

  function getSignupFormErrors(firstname, email, password, reenterPassword) {
    let errors = [];

    // Clear previous error highlights
    [firstname_input, email_input, password_input, re_enter_password_input].forEach(input => {
      input.classList.remove('incorrect');
    });

    if (!firstname) {
      errors.push('First name is required');
      firstname_input.classList.add('incorrect');
    }

    if (!email) {
      errors.push('Email is required');
      email_input.classList.add('incorrect');
    } else {
      // Email format check
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        errors.push('Invalid email format');
        email_input.classList.add('incorrect');
      }
    }

    if (!password) {
      errors.push('Password is required');
      password_input.classList.add('incorrect');
    } else if (password.length < 8) {
      errors.push('Password must be at least 8 characters');
      password_input.classList.add('incorrect');
    }

    if (password !== reenterPassword) {
      errors.push('Passwords do not match');
      password_input.classList.add('incorrect');
      re_enter_password_input.classList.add('incorrect');
    }

    return errors;
  }

  // Clear error and success messages on input change
  [firstname_input, email_input, password_input, re_enter_password_input].forEach(input => {
    input.addEventListener('input', () => {
      input.classList.remove('incorrect');
      error_message.innerText = '';
      success_message.innerText = '';
    });
  });
});
