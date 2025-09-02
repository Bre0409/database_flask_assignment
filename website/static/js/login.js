

// LOGIN FORM VALIDATION
document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById('login-form');
  if (!loginForm) return;  // Only run on login page

  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');

  // Create message containers if not present
  let errorMessage = document.getElementById('login-error-message');
  let successMessage = document.getElementById('login-success-message');

  if (!errorMessage) {
    errorMessage = document.createElement('div');
    errorMessage.id = 'login-error-message';
    errorMessage.style.color = 'red';
    loginForm.appendChild(errorMessage);
  }

  if (!successMessage) {
    successMessage = document.createElement('div');
    successMessage.id = 'login-success-message';
    successMessage.style.color = 'green';
    loginForm.appendChild(successMessage);
  }

  loginForm.addEventListener('submit', function (e) {
    let errors = [];

    // Clear previous error highlights
    [emailInput, passwordInput].forEach(input => input.classList.remove('incorrect'));

    if (!emailInput.value.trim()) {
      errors.push('Email is required');
      emailInput.classList.add('incorrect');
    }

    if (!passwordInput.value.trim()) {
      errors.push('Password is required');
      passwordInput.classList.add('incorrect');
    }

    if (errors.length > 0) {
      e.preventDefault();
      errorMessage.innerHTML = errors.join('<br>');
      successMessage.innerText = '';
    } else {
    
    }
  });

  // Clear messages on input
  [emailInput, passwordInput].forEach(input => {
    input.addEventListener('input', () => {
      input.classList.remove('incorrect');
      errorMessage.innerText = '';
      successMessage.innerText = '';
    });
  });
});