window.addEventListener('offline', function () {
  alert("You are offline!");
});

var preloader;

function preloader() {
  preloader = setTimeout(showPage, 3000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  //$("#loader").hide();
  document.getElementById("myDiv").style.display = "block";
  //$("#myDev").show();
}

$(document).ready(function () {

  $(".overlay").hide();

  var wl = window.location.href;
  if (wl.indexOf("/api") > 0) {
    getBid();
  }

  function getBid() {
    var bid = $("#bid_inp").val();
    $.ajax({
      url: "/getReview",
      method: "POST",
      data: {
        bid: bid
      },
      success: function (data) {
        $("#reviews").html(data);
      }
    })
  }

  $("#reviewForm").on("submit", function (e) {
    e.preventDefault();
    $(".overlay").show();
    $.ajax({
      url: "/review",
      method: "POST",
      data: $("#reviewForm").serialize(),
      success: function (data) {
        getBid();
        $(".overlay").hide();
        if (data == "reviewed") {
          $("#rfta").val('');
        } else if (data != "reviewed") {
          $(".e_msg").text(data);
        }
      }
    })
  })

  setInterval(() => {
    if ($.trim($(".e_msg").text()) != '') {
      $(".e_msg").text('');
    };
  },
    10000);
})