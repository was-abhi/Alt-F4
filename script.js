document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        displayMessage(messageText, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageText })
            });
            const data = await response.json();
            displayMessage(data.reply, 'bot');
        } catch (error) {
            console.error('Error fetching chat response:', error);
            displayMessage("MovBot is having trouble connecting. Please try again later.", 'bot');
        }
    }

    function displayMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender + '-message');

        const messageContentDiv = document.createElement('div');
        messageContentDiv.classList.add('message-content');
        messageContentDiv.textContent = text;

        messageDiv.appendChild(messageContentDiv);
        chatMessages.appendChild(messageDiv);
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
