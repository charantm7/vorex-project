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
