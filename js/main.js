$(document).ready(function () {
  $(".login-btn").on("click", function () {
    $(".login-modal").css("display", "flex");
  })
  $(".login-close").on("click", function () {
    $(".login-modal").css("display", "none");
  })

  $(".reg-btn").on("click", function () {
    $(".reg-modal").css("display", "flex");
  })
  $(".reg-close").on("click", function () {
    $(".reg-modal").css("display", "none");
  })
})