window.addEventListener('offline', function () {
  alert("You are offline!");
});

$(document).ready(function () {

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
})