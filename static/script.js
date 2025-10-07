const form = document.getElementById("my-form");
const usernameInput = document.getElementById("register-username");
const passwordInput = document.getElementById("register-password");
const confirmPasswordInput = document.getElementById("confirm-password");

form.addEventListener("submit", (e) => {
  if (passwordInput.value != confirmPasswordInput.value) {
    e.preventDefault();
    // might change alert to pop up later or nothing at all
    alert("Passwords do not match!");
    passwordInput.value = "";
    confirmPasswordInput.value = "";
  }
});
