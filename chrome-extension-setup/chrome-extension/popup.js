document.getElementById('userInput').addEventListener('keydown', function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById('send').click();
    }
});

document.getElementById('send').addEventListener('click', function () {
    let userInput = document.getElementById('userInput').value;
    updateChatHistory("user", userInput);

    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_input: userInput
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(text => {
        try {
            const data = JSON.parse(text);
            updateChatHistory("bot", data.response);
        } catch (error) {
            console.error('Failed to parse JSON:', error);
            throw new Error('Failed to parse JSON');
        }
    })
    .catch(error => console.error('Error:', error));

    // Clear the input field after sending the message
    document.getElementById('userInput').value = "";
});

function updateChatHistory(role, message) {
    const chatHistory = document.getElementById('chatHistory');
    const messageDiv = document.createElement('div');
    if (role === "user") {
        messageDiv.className = "userMessage";
    } else {
        messageDiv.className = "botMessage";
    }
    messageDiv.textContent = message;
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
