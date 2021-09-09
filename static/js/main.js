// 화면 전환
jQuery(function($) {
  $("body").css("display", "none");
  $("body").fadeIn(800);
  $("a.transition").click(function(event){
    event.preventDefault();
    linkLocation = this.href;
    $("body").fadeOut(800, redirectPage);
  });
  function redirectPage() {
    window.location = linkLocation;
  }
});