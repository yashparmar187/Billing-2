document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tabs
    const tabTriggerList = document.querySelectorAll('[data-bs-toggle="tab"]');
    [...tabTriggerList].forEach(tabTriggerEl => {
      new bootstrap.Tab(tabTriggerEl);
    });
  
    // Ensure tab switching works with anchor links
    document.querySelectorAll('.switch-tab').forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const tab = new bootstrap.Tab(this);
        tab.show();
        console.log('Switching to tab:', this.getAttribute('data-bs-target'));
      });
    });
  
    // Login form submission
    const loginForm = document.querySelector('#login form');
    if (loginForm) {
      loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        console.log('Login attempt:', { email, password });
        // Add login logic here
      });
    }
  
    // Register form submission
    const registerForm = document.querySelector('#register form');
    if (registerForm) {
      registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const accountType = document.querySelector('input[name="accountType"]:checked').value;
        const profilePhoto = document.getElementById('profilePhoto').files[0];
        if (password !== confirmPassword) {
          alert('Passwords do not match!');
          return;
        }
        console.log('Registration attempt:', { email, username, password, accountType, profilePhoto });
        // Add registration logic here
      });
    }
  });