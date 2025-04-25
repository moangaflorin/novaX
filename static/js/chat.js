document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const userIdDisplay = document.getElementById('user-id-display');
    const logoutButton = document.getElementById('logout-button'); 

    
    const userId = `User_${Math.floor(Math.random() * 1000)}`;
    userIdDisplay.textContent = `ID: ${userId}`;

    const channel = new BroadcastChannel('chatroom_channel');

    const displayMessage = (messageData) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');

        const senderSpan = document.createElement('span');
        senderSpan.classList.add('sender');

        const timestampSpan = document.createElement('span');
        timestampSpan.classList.add('timestamp');
        timestampSpan.textContent = new Date(messageData.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        if (messageData.sender === userId) {
            messageElement.classList.add('own-message');
            senderSpan.textContent = 'You'; 
        } else {
            messageElement.classList.add('other-message');
            senderSpan.textContent = messageData.sender;
        }

        const textNode = document.createTextNode(messageData.text);

        messageElement.appendChild(senderSpan);
        messageElement.appendChild(textNode);
        messageElement.appendChild(timestampSpan);

        messagesContainer.appendChild(messageElement);

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    const sendMessage = () => {
        const messageText = messageInput.value.trim();
        if (messageText === '') return;

        const messageData = {
            sender: userId,
            text: messageText,
            timestamp: Date.now()
        };

        displayMessage(messageData);

        channel.postMessage(messageData);

        messageInput.value = '';
        messageInput.focus();
    };

    channel.onmessage = (event) => {
        const messageData = event.data; 
        if (messageData.sender !== userId) {
            displayMessage(messageData);
        }
    };

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    logoutButton.addEventListener('click', () => {
        window.location.href = '/';
    });

     messageInput.focus();
});