$(document).ready(function () {
  $(".login-btn").on("click", function () {
    $(".login-modal").css("display", "flex");
  })
  $(".modal-close").on("click", function () {
    $(".modal").css("display", "none");
  })

  $(".reg-btn").on("click", function () {
    $(".reg-modal").css("display", "flex");
  })
  $(".modal-close").on("click", function () {
    $(".modal").css("display", "none");
  })
})