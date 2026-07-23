document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".nav-tab");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", function (event) {
            event.preventDefault();

            // Remove 'active' class from all tabs
            tabs.forEach(t => t.classList.remove("active"));
            this.classList.add("active");

            // Hide all tab content
            contents.forEach(content => content.classList.remove("active-content"));

            // Show the content associated with the clicked tab
            const targetId = this.getAttribute("data-tab");
            document.getElementById(targetId).classList.add("active-content");
        });
    });

    // Chatbot functionality
    const chatbotContainer = document.querySelector(".chatbot-container");
    const chatbotMessages = document.querySelector(".chatbot-messages");
    const chatbotInput = document.querySelector("#chatbot-input");
    const chatbotSend = document.querySelector("#chatbot-send");
    const chatbotToggle = document.querySelector(".chatbot-toggle");

    // Toggle chatbot visibility
    chatbotToggle.addEventListener("click", function () {
        chatbotContainer.classList.toggle("minimized");
        chatbotToggle.textContent = chatbotContainer.classList.contains("minimized") ? "+" : "−";
    });

    // Function to add a message to the chat
    function addMessage(text, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chatbot-message", sender);
        messageElement.textContent = text;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Handle sending messages
    chatbotSend.addEventListener("click", function () {
        sendMessage();
    });

    chatbotInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (message === "") return;

        // Add user message to chat window
        addMessage(message, "user");

        // Clear input field
        chatbotInput.value = "";

        // Send request to Flask backend
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response, "bot");
            } else {
                addMessage("Error: No response from the server.", "bot");
            }
        })
        .catch(error => {
            addMessage("Error: Unable to connect to chat server.", "bot");
            console.error("Chatbot Error:", error);
        });
    }
});

