const sidebar = document.getElementById("sidebar");
const menuBtn = document.getElementById("menuBtn");

menuBtn.addEventListener("click", () => {
  sidebar.classList.toggle("active");
});
function myFunction(x) {
  x.classList.toggle("change");
}

// window.addEventListener("load", () => {
//   setTimeout(() => {
//     const preloader = document.getElementById("preloader");
//     preloader.style.opacity = "0";
//     setTimeout(() => {
//       preloader.style.display = "none";
//     }, 100);
//   }, 500);
// });
