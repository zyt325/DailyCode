var container = document.getElementById("container");
container.style.width = window.innerWidth * 0.9 + "px";
//container.style.height = window.innerHeight * 1 + 'px';
container.style.marginLeft = "auto";
container.style.marginRight = "auto";
var article_list = document.getElementById("article_list");
article_list.style.width = window.innerWidth * 0.9 - 40 + "px";

function article_edit(obj) {
  article_id = obj.getAttribute("article_id");
  class_id = obj.getAttribute("class_id");
  url = "/#/edit/?id=" + article_id;
  window.location.href = url;
}

function loadScript(url) {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = url;
  document.body.appendChild(script);
}

function goTop() {
  document.body.scrollTop = document.documentElement.scrollTop = 0;
}

function add_goTop() {
  var container = document.getElementById("container");
  var top_ico = document.createElement("button");
  top_ico.id = "goTop";
  top_ico.textContent = "TOP";
  top_ico.onclick = goTop;
  top_ico.setAttribute(
    "style",
    "position:fixed;bottom:40px;right:0;border-width:0;width:40px;height:40px;font-size:16px;background-color:#D4E6EB"
  );
  container.appendChild(top_ico);
}

loadScript("http://lib.personer.website/js/ajax.js");
loadScript("http://lib.personer.website/js/common.js");

window.onload = function () {
  //login_auth();
  add_goTop();
};
