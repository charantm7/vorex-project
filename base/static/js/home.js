var modal = document.getElementById("id01");
const home = document.querySelector(".main-body");
// When the user clicks anywhere outside of the modal, close it

document.addEventListener("DOMContentLoaded", () => {
  const queryParams = new URLSearchParams(window.location.search);
  const action = queryParams.get("action");

  if (action === "create") {
    modal.style.display = "block";
  } else if (action === "cancel") {
    modal.style.display = "none";
    home.classList.add("active");
  }
});
