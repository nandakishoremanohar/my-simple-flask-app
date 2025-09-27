// Basic client-side validation (optional)

document.addEventListener('DOMContentLoaded', () => {
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
      const username = signupForm.username.value.trim();
      const email = signupForm.email.value.trim();
      const password = signupForm.password.value.trim();

      if (!username || !email || !password) {
        e.preventDefault();
        alert("Please fill out all fields.");
      }
    });
  }

  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      const email = loginForm.email.value.trim();
      const password = loginForm.password.value.trim();

      if (!email || !password) {
        e.preventDefault();
        alert("Please fill out both fields.");
      }
    });
  }
});
