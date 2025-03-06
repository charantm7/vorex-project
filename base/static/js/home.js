function openModal() {
  window.location.href = "create_room/";
}

function openYourRoom() {
  let url = document.getElementById("OpenYourRooms").getAttribute("data-url");
  window, (location.href = url);
}

function openJoinedRoom() {
  window.location.href = "joined-room/";
}
