window.addEventListener('offline', function () {
  alert("You are offline!");
});

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

  $("#loginForm").on("submit", function () {
    $(".overlay").show();
    $.ajax({
      url: "/login",
      method: "POST",
      data: $("#loginForm").serialize(),
      success: function (data) {
        $(".overlay").hide();
        if (data == "Login successful!") {
          window.location = "/";
        } else if (data != "Login successful!") {
          alert(data);
        }
      }
    })
  })

  // get books within 2020 - 2015
  getBook2020();
  function getBook2020() {
    $(".overlay").show();
    $.ajax({
      url: "/getBooks",
      method: "POST",
      data: {yearR:2020},
      success: function (data) {
        $(".overlay").hide();
        $("#getBook2020").html(data);
      }
    })
  }

})