window.addEventListener("scroll", function() {
  updateNavbar();
});

function updateNavbar() {
  if (document.body.scrollTop > 10 || document.documentElement.scrollTop > 10) {
    document.getElementById("main-nav").classList.add("sticky");
  } else {
    document.getElementById("main-nav").classList.remove("sticky");
  }
}
