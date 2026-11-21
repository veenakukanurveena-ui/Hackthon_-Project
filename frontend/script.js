// SentinelOps - Dashboard JavaScript

document.addEventListener("DOMContentLoaded", function () {

  // Update current date and time
  function updateDateTime() {
      const dateElement = document.getElementById("current-date");

      if (dateElement) {
          const now = new Date();

          dateElement.textContent = now.toLocaleDateString("en-IN", {
              day: "2-digit",
              month: "short",
              year: "numeric"
          });
      }
  }

  updateDateTime();

  // Highlight active sidebar link
  const navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach(function (link) {
      const linkPage = link.getAttribute("href");
      const currentPage = window.location.pathname;

      if (
          linkPage &&
          currentPage.endsWith(linkPage.replace("./", ""))
      ) {
          navLinks.forEach(function (item) {
              item.classList.remove("active");
          });

          link.classList.add("active");
      }
  });

  // Notification button
  const notificationButton = document.querySelector(".icon-button");

  if (notificationButton) {
      notificationButton.addEventListener("click", function () {
          alert("SentinelOps: No new notifications.");
      });
  }

  // Display dashboard status
  console.log("SentinelOps dashboard loaded successfully.");

});