document.addEventListener("DOMContentLoaded", () => {

  // Initialize icons
  if (window.lucide) {
      lucide.createIcons();
  }

  // Elements
  const loginForm = document.getElementById("loginForm");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const togglePassword = document.getElementById("togglePassword");
  const loginButton = document.querySelector(".login-button");
  const loginMessage = document.getElementById("loginMessage");
  const rememberMe = document.getElementById("rememberMe");

  // Password visibility
  togglePassword.addEventListener("click", () => {

      const isPassword = passwordInput.type === "password";

      passwordInput.type = isPassword ? "text" : "password";

      togglePassword.innerHTML = isPassword
          ? '<i data-lucide="eye-off"></i>'
          : '<i data-lucide="eye"></i>';

      togglePassword.setAttribute(
          "aria-label",
          isPassword ? "Hide password" : "Show password"
      );

      if (window.lucide) {
          lucide.createIcons();
      }
  });


  // Clear messages when user types
  emailInput.addEventListener("input", clearMessage);
  passwordInput.addEventListener("input", clearMessage);

  function clearMessage() {
      loginMessage.textContent = "";
  }


  // Login form validation
  loginForm.addEventListener("submit", (event) => {

      event.preventDefault();

      const email = emailInput.value.trim();
      const password = passwordInput.value;

      loginMessage.style.color = "#ff9e9e";

      // Email validation
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!emailPattern.test(email)) {
          loginMessage.textContent = "Please enter a valid email address.";
          emailInput.focus();
          return;
      }

      // Password validation
      if (password.length < 8) {
          loginMessage.textContent =
              "Password must contain at least 8 characters.";
          passwordInput.focus();
          return;
      }

      // Loading state
      loginButton.disabled = true;
      loginButton.style.opacity = "0.75";

      loginButton.innerHTML = `
          <span>AUTHENTICATING...</span>
          <i data-lucide="loader-circle" class="loading-icon"></i>
      `;

      if (window.lucide) {
          lucide.createIcons();
      }

      // Temporary frontend demonstration
      setTimeout(() => {

          loginButton.disabled = false;
          loginButton.style.opacity = "1";

          loginButton.innerHTML = `
              <span>ACCESS WORKSPACE</span>
              <i data-lucide="arrow-up-right"></i>
              <div class="button-glow"></div>
          `;

          if (window.lucide) {
              lucide.createIcons();
          }

          loginMessage.style.color = "#ffca70";

          loginMessage.textContent =
              "Login interface ready. Backend authentication is not connected yet.";

      }, 1200);

      // Remember-me preference is only a UI choice at this stage.
      console.log("Remember me:", rememberMe.checked);

  });


  // Animated background particles
  const particlesContainer = document.getElementById("particles");

  if (particlesContainer) {

      for (let i = 0; i < 35; i++) {

          const particle = document.createElement("span");

          particle.className = "particle";

          particle.style.left = Math.random() * 100 + "%";
          particle.style.top = Math.random() * 100 + "%";
          particle.style.animationDelay = Math.random() * 8 + "s";
          particle.style.animationDuration =
              (5 + Math.random() * 8) + "s";

          particlesContainer.appendChild(particle);

      }

  }

});