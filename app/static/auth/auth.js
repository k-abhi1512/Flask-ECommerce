const API_URL = 'http://localhost:5001/auth';

// Handle Registration
const registerForm = document.getElementById('register-form');
if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (password !== confirmPassword) {
      document.getElementById('register-message').textContent = 'Passwords do not match.';
      document.getElementById('register-message').style.color = 'red';
      return;
    }

    try {
      const response = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      document.getElementById('register-message').textContent = data.message;
      document.getElementById('register-message').style.color = response.ok ? 'green' : 'red';

      if (response.ok) {
        setTimeout(() => {
          window.location.href = 'login.html';
        }, 1500);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });
}

// Handle Login
const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      document.getElementById('login-message').textContent = data.message;
      document.getElementById('login-message').style.color = response.ok ? 'green' : 'red';

      if (response.ok) {
        localStorage.setItem('token', data.token); // Store token
        setTimeout(() => {
          window.location.href = 'dashboard.html'; // Redirect after login
        }, 1500);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });
}
