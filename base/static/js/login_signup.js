function togglePassword(fieldId) {
  var passwordField = document.getElementById(fieldId);
  var hideIcon = document.getElementById("hide-" + fieldId);
  var showIcon = document.getElementById("show-" + fieldId);

  if (passwordField.type === "password") {
    passwordField.type = "text";
    hideIcon.style.display = "none";
    showIcon.style.display = "block";
  } else {
    passwordField.type = "password";
    hideIcon.style.display = "block";
    showIcon.style.display = "none";
  }
}
