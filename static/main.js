window.addEventListener('offline', function () {
  alert("You are offline!")
});

window.addEventListener('online', function () {

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
        url: "/action",
        method: "POST",
        data: $("#loginForm").serialize(),
        success: function (data) {
          $(".overlay").hide();
          if (data == "Login successful!") {
            alert(data);
            window.location = "/";
          } else if (data != "Login successful!") {
            alert(data);
          }
        }
      })
    })

  })
})