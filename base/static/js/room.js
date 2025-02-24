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
    document.getElementById("Group").style.overflow = "hidden";
  }
  document.getElementById(cityName).style.display = "flex";
  evt.currentTarget.className += " active";
}
document.getElementById("defaultOpen").click();

function loadMessages(roomName, chatType, chatId) {
  fetch(`/fetch-messages/${roomName}/${chatType}/${chatId}/`)
    .then((response) => response.json())
    .then((data) => {
      const chatArea = document.getElementById("chat-area-mid");
      chatArea.innerHTML = ""; // Clear existing messages

      data.messages.forEach((msg) => {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("chat-message");
        msgDiv.innerHTML = `<strong>${msg.user}:</strong> ${msg.content} <span class="time">${msg.created_at}</span>`;
        chatArea.appendChild(msgDiv);
      });
    })
    .catch((error) => console.error("Error loading messages:", error));
}
