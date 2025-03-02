document.addEventListener("DOMContentLoaded", function () {
  const savedTab = localStorage.getItem("activeTab");

  if (savedTab) {
    const tabButton = document.querySelector(`[onclick="openTab(event, '${savedTab}')"]`);
    if (tabButton) {
      tabButton.click();
    }
  } else {
    document.getElementById("defaultOpen").click();
  }
});

function openTab(evt, cityName) {
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  if (cityName === "Group") {
    document.getElementById("Group").style.overflow = "hidden !important";
  }

  document.getElementById(cityName).style.display = "flex";
  evt.currentTarget.className += " active";

  localStorage.setItem("activeTab", cityName);
}

document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);
  const tabName = params.get("tab");

  if (tabName) {
    const tabButton = document.querySelector(`[onclick="openTab(event, '${tabName}')"]`);
    if (tabButton) {
      tabButton.click();
    }
  } else {
    document.getElementById("defaultOpen").click();
  }
});

// function openChat(username) {
//   // Change chat title
//   document.getElementById("chat-title").innerText = username + "'s Chat";

//   // Hide sidebar & show chat area on mobile
//   if (window.innerWidth <= 768) {
//     document.querySelector(".sidebarc").style.display = "none";
//     document.querySelector(".chat-area").style.display = "block";
//   }
// }

// // Back to sidebar on mobile
// function backToSidebar() {
//   document.querySelector(".sidebarc").style.display = "block";
//   document.querySelector(".chat-area").style.display = "none";
// }

function showIndividualChats() {
  document.getElementById("individual-chats").style.display = "block";
  document.getElementById("group-chats").style.display = "none";
}

function showGroupChats() {
  document.getElementById("individual-chats").style.display = "none";
  document.getElementById("group-chats").style.display = "block";
}

function openChat(name) {
  document.getElementById("chat-title").textContent = name;
  document.getElementById("chat-messages").innerHTML = `<p>Chat with ${name}</p>`;

  // Show chat area and hide sidebar on mobile
  if (window.innerWidth <= 768) {
    document.querySelector(".sidebarc").style.display = "none";
    document.querySelector(".chat-area").style.display = "flex";
  }
}

function backToSidebar() {
  document.querySelector(".sidebarc").style.display = "block";
  document.querySelector(".chat-area").style.display = "none";
}

function sendMessage() {
  let message = document.getElementById("message-input").value;
  if (message.trim() !== "") {
    let messageDiv = document.createElement("div");
    messageDiv.textContent = message;
    messageDiv.style.padding = "10px";
    messageDiv.style.background = "#dff9fb";
    messageDiv.style.margin = "5px 0";
    messageDiv.style.borderRadius = "5px";

    document.getElementById("chat-messages").appendChild(messageDiv);
    document.getElementById("message-input").value = "";

    // Auto-scroll to the latest message
    let chatMessages = document.getElementById("chat-messages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}
