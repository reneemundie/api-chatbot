$(document).ready(function() {
  $("#send-button").click(function() {
    sendMessage();
  });

  $("#text").keypress(function(e) {
    if (e.keyCode == 13) {
      e.preventDefault();
      sendMessage();
    }
  });

  function sendMessage() {
    var message = $("#text").val();
    $("#text").val("");

    $.ajax({
      type: "POST",
      url: "/",
      contentType: "application/json",
      data: JSON.stringify({ message: message }),
      success: function(response) {
        var bot_response = response.response;
        $(".chat-box").append(createMessageElement("You", message, "you"));
        $(".chat-box").append(createMessageElement("Go Travel", bot_response, "bot"));
        $(".chat-box").scrollTop($(".chat-box")[0].scrollHeight);
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  function createMessageElement(sender, message, cssClass) {
    var div = $("<div>").addClass("chat-message " + cssClass);
    var senderSpan = $("<span>").addClass("sender").text(sender + ": ");
    var messageSpan = $("<span>").addClass("message").text(message);
    div.append(senderSpan).append(messageSpan);
    return div;
  }
});