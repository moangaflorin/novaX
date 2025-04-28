document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const userIdDisplay = document.getElementById('user-id-display');
    const logoutButton = document.getElementById('logout-button'); 
    
    // Get username from localStorage or redirect if not logged in
    const username = localStorage.getItem('chatUsername');
    if (!username) {
        console.error("No username found in localStorage, redirecting to login");
        window.location.href = '/';
        return;
    }
    
    // Add connection status indicator
    const statusIndicator = document.createElement('div');
    statusIndicator.id = 'connection-status';
    statusIndicator.textContent = 'Connecting...';
    statusIndicator.style.textAlign = 'center';
    statusIndicator.style.padding = '5px';
    statusIndicator.style.backgroundColor = '#ffc107';
    messagesContainer.parentNode.insertBefore(statusIndicator, messagesContainer);
    
    // Display the real username instead of a random ID
    userIdDisplay.textContent = `Logged in as: ${username}`;

    // Store pending messages while reconnecting
    let pendingMessages = [];
    let isReconnecting = false;
    
    // WebSocket connection with real username
    let socket;
    let isConnected = false;
    
    // Function to establish WebSocket connection
    function connectWebSocket() {
        socket = new WebSocket(`ws://${window.location.host}/ws/${username}`);
        
        socket.onopen = () => {
            console.log('WebSocket connection established');
            isConnected = true;
            statusIndicator.textContent = 'Connected';
            statusIndicator.style.backgroundColor = '#28a745';
            
            // Send any pending messages that accumulated while disconnected
            if (pendingMessages.length > 0) {
                console.log(`Sending ${pendingMessages.length} pending messages`);
                pendingMessages.forEach(msg => {
                    socket.send(JSON.stringify(msg));
                });
                pendingMessages = [];
            }
            
            isReconnecting = false;
        };

        socket.onclose = (event) => {
            console.log('WebSocket connection closed:', event.reason);
            isConnected = false;
            
            // Don't show disconnected message during page unload
            if (isPageUnloading) return;
            
            statusIndicator.textContent = 'Disconnected - Attempting to reconnect...';
            statusIndicator.style.backgroundColor = '#dc3545';
            
            // If the server closed the connection due to a new login
            if (event.reason === 'Logged in from another session') {
                const messageElement = document.createElement('div');
                messageElement.classList.add('system-message');
                messageElement.textContent = 'You have been disconnected because you logged in from another session.';
                messagesContainer.appendChild(messageElement);
                return; // Don't attempt to reconnect in this case
            }
            
            // Attempt to reconnect if not already reconnecting
            if (!isReconnecting) {
                isReconnecting = true;
                // Wait a moment before reconnecting to avoid rapid reconnection attempts
                setTimeout(connectWebSocket, 2000);
            }
        };

        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            statusIndicator.textContent = 'Connection Error';
            statusIndicator.style.backgroundColor = '#dc3545';
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Received message:', data);
            
            // Handle different message types
            if (data.type === 'history') {
                // Display message history
                displayMessageHistory(data.messages);
            } else {
                // Handle system message or regular message
                displayMessage(data);
            }
        };
    }
    
    // Initialize connection
    connectWebSocket();

    const displayMessage = (messageData) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');

        // Handle system messages differently
        if (messageData.type === 'system') {
            messageElement.classList.add('system-message');
            messageElement.textContent = messageData.text;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            return;
        }

        const senderSpan = document.createElement('span');
        senderSpan.classList.add('sender');

        const timestampSpan = document.createElement('span');
        timestampSpan.classList.add('timestamp');
        timestampSpan.textContent = new Date(messageData.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        if (messageData.sender === username) {
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

    // Display message history
    const displayMessageHistory = (messages) => {
        messagesContainer.innerHTML = '';
        messages.forEach(message => {
            displayMessage(message);
        });
    };

    const sendMessage = () => {
        const messageText = messageInput.value.trim();
        if (messageText === '') return;

        const messageData = {
            sender: username,
            text: messageText,
            timestamp: Date.now()
        };

        // Display own message immediately
        displayMessage(messageData);

        // If connected, send immediately, otherwise queue for later sending
        if (isConnected) {
            socket.send(JSON.stringify(messageData));
        } else {
            pendingMessages.push(messageData);
            console.log("Connection lost, message queued for later sending");
        }

        messageInput.value = '';
        messageInput.focus();
    };

    // Add CSS for system messages
    const style = document.createElement('style');
    style.textContent = `
        .system-message {
            text-align: center;
            background-color: #f0f0f0;
            color: #666;
            font-style: italic;
            padding: 5px;
            margin: 5px 0;
            border-radius: 5px;
            font-size: 0.9em;
        }
    `;
    document.head.appendChild(style);

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Track page unloading
    let isPageUnloading = false;
    
    window.addEventListener('beforeunload', () => {
        isPageUnloading = true;
        // Close socket gracefully if possible
        if (socket && isConnected) {
            socket.close(1000, "Page refresh or navigation");
        }
    });

    logoutButton.addEventListener('click', () => {
        isPageUnloading = true;
        if (socket && isConnected) {
            socket.close(1000, "User logout");
        }
        // Clear username from localStorage on logout
        localStorage.removeItem('chatUsername');
        window.location.href = '/';
    });

    messageInput.focus();
});