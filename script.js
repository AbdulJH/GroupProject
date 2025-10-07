const form = document.getElementById("my-form");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirm-password");

form.addEventListener("submit", (e) => {
  if (passwordInput.value != confirmPasswordInput.value) {
    e.preventDefault();
    // i can change this to an html pop up later or clear the passwords or both
    alert("Passwords do not match!");
    passwordInput.value = "";
    confirmPasswordInput.value = "";
  } else {
    alert("Form submitted!!");
  }
});
