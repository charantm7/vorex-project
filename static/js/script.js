const sidebar = document.getElementById("sidebar");
const menuBtn = document.getElementById("menuBtn");

menuBtn.addEventListener("click", () => {
  sidebar.classList.toggle("active");
});
function myFunction(x) {
  x.classList.toggle("change");
}
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-50px";
  }
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
