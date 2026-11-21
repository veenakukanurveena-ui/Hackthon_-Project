document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("registerForm");
  const fullName = document.getElementById("fullName");
  const email = document.getElementById("registerEmail");
  const password = document.getElementById("registerPassword");
  const confirmPassword = document.getElementById("confirmPassword");
  const acceptTerms = document.getElementById("acceptTerms");
  const message = document.getElementById("registerMessage");
  const button = document.getElementById("registerButton");
  const togglePassword = document.getElementById("toggleRegisterPassword");

  // SHOW / HIDE PASSWORD
  togglePassword.addEventListener("click", () => {
      const isHidden = password.type === "password";
      password.type = isHidden ? "text" : "password";

      togglePassword.innerHTML = isHidden
          ? '<i data-lucide="eye-off"></i>'
          : '<i data-lucide="eye"></i>';

      if (window.lucide) lucide.createIcons();
  });

  // DISPLAY MESSAGE
  function showMessage(text, type) {
      message.textContent = text;
      message.className = "register-message " + type;
  }

  // CLEAR MESSAGE
  [fullName, email, password, confirmPassword].forEach(input => {
      input.addEventListener("input", () => {
          message.className = "register-message";
      });
  });

  // REGISTRATION
  form.addEventListener("submit", (event) => {
      event.preventDefault();

      const nameValue = fullName.value.trim();
      const emailValue = email.value.trim().toLowerCase();
      const passwordValue = password.value;
      const confirmValue = confirmPassword.value;

      message.className = "register-message";

      // 1. EMPTY FIELD CHECK
      if (!nameValue || !emailValue || !passwordValue || !confirmValue) {
          showMessage("Please fill in all fields.", "error");
          return;
      }

      // 2. NAME: LETTERS AND SPACES ONLY
      const namePattern = /^[A-Za-z]+(?:\s+[A-Za-z]+)*$/;

      if (!namePattern.test(nameValue)) {
          showMessage(
              "Name must contain letters and spaces only. Numbers and special characters are not allowed.",
              "error"
          );
          fullName.focus();
          return;
      }

      // 3. EMAIL: PROPER FORMAT
      const emailPattern =
          /^[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$/;

      if (!emailPattern.test(emailValue)) {
          showMessage(
              "Please enter a valid email address, for example name@gmail.com.",
              "error"
          );
          email.focus();
          return;
      }

      // 4. STRONG PASSWORD
      const passwordPattern =
          /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

      if (!passwordPattern.test(passwordValue)) {
          showMessage(
              "Password needs 8+ characters, uppercase, lowercase, number and special character.",
              "error"
          );
          password.focus();
          return;
      }

      // 5. CONFIRM PASSWORD
      if (passwordValue !== confirmValue) {
          showMessage("Passwords do not match.", "error");
          confirmPassword.focus();
          return;
      }

      // 6. TERMS CHECK
      if (!acceptTerms.checked) {
          showMessage("Please accept the Terms and Privacy Policy.", "error");
          return;
      }

      // 7. GET EXISTING USERS
      let users = [];

      try {
          users = JSON.parse(localStorage.getItem("sentinelUsers")) || [];

          if (!Array.isArray(users)) {
              showMessage("Account data is invalid.", "error");
              return;
          }
      } catch (error) {
          showMessage("Unable to read account data.", "error");
          return;
      }

      // 8. DUPLICATE EMAIL CHECK
      if (users.some(user => user.email === emailValue)) {
          showMessage("This email is already registered. Please log in.", "error");
          email.focus();
          return;
      }

      // 9. CREATE ACCOUNT
      // Temporary frontend demo only. Do not use plaintext passwords in production.
      const newUser = {
          id: Date.now(),
          name: nameValue,
          email: emailValue,
          password: passwordValue,
          createdAt: new Date().toISOString()
      };

      users.push(newUser);

      // 10. SAVE ACCOUNT
      try {
          localStorage.setItem("sentinelUsers", JSON.stringify(users));
      } catch (error) {
          showMessage("Unable to save account. Please check browser storage.", "error");
          return;
      }

      // 11. SUCCESS
      button.disabled = true;
      button.textContent = "ACCOUNT CREATED ✓";

      showMessage("Account created successfully! Redirecting to login...", "success");

      setTimeout(() => {
          window.location.href = "login.html";
      }, 1800);

  });

});