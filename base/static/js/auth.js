const wrapper = document.querySelector(".wrapper");
const registerLink = document.querySelector(".register-link");
const loginLink = document.querySelector(".login-link");
const thirdPartyAuthLogin = document.querySelector("#third-party-login");
const thirdPartyAuthRegister = document.querySelector("#third-party-register");

registerLink.onclick = () => {
  wrapper.classList.add("active");
  thirdPartyAuthLogin.classList.remove("active");
};

loginLink.onclick = () => {
  wrapper.classList.remove("active");
  thirdPartyAuthRegister.classList.remove("active");
};

document.addEventListener("DOMContentLoaded", () => {
  const queryParams = new URLSearchParams(window.location.search);
  const action = queryParams.get("action");

  if (action === "signup") {
    wrapper.classList.add("active");
    thirdPartyAuthLogin.classList.remove("active");
  } else if (action === "login") {
    wrapper.classList.remove("active");
    thirdPartyAuthRegister.classList.remove("active");
  }
});
