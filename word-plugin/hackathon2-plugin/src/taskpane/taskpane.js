// taskpane.js
Office.onReady(() => {
  $(document).ready(() => {
    $("#send-button").click(async () => {
      const userInput = $("#message-input").val();
      if (userInput) {
        appendMessage("You", userInput); // Display user input
        $("#message-input").val(""); // Clear input field

        // Query the FastAPI endpoint
        try {
          const response = await fetch(
            "http://localhost:8000/query/?query=" +
              encodeURIComponent(userInput)
          );
          if (!response.ok) throw new Error("Network response was not ok");

          const data = await response.json();
          appendMessage("Bot", JSON.stringify(data)); // Display response from API
        } catch (error) {
          console.error("Error fetching from API:", error);
          appendMessage("Error", "Failed to fetch from API.");
        }
      }
    });
  });
});

// Function to append messages to the chat box
function appendMessage(sender, message) {
  $("#chat-box").append(`<p><strong>${sender}:</strong> ${message}</p>`);
  $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight); // Auto-scroll to bottom
}
