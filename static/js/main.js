window.addEventListener('offline', function () {
  alert("You are offline!");
});

$(document).ready(function () {

  var wl = window.href;
  alert (wl);
  getBid();
  function getBid() {
    alert();
    $("#bid").submit();
  }

  $("#bid").on("submit", function getReview(e) {
    e.preventDefault();
    $(".overlay").show();
    $.ajax({
      url: "/getReview",
      method: "POST",
      data: $("#bid").serialize(),
      success: function (data) {
        $("#reviews").html(data);
        $(".overlay").hide();
      }
    })
  })

  $("#reviewForm").on("submit", function (e) {
    e.preventDefault();
    $(".overlay").show();
    $.ajax({
      url: "/review",
      method: "POST",
      data: $("#reviewForm").serialize(),
      success: function (data) {
        getBid();
        //$(".overlay").hide();
        if (data == "reviewed") {
          alert(data);
        } else if (data != "reviewed") {
          alert(data);
        }
      }
    })
  })
})