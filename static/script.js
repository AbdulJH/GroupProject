const form = document.getElementById("my-form");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
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
