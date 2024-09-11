function onLoaded(event){
    const chatInputField = document.querySelector('.chat-input');
    const sendButton = document.querySelector('.chat-send-btn');
    const chatMessages = document.querySelector('.chat-messages');
    
    // ---- PROCESS USER EVENTS ----
    function process_send_event(e){
        e.preventDefault();
        const message_to_send = chatInputField.value.trim();
        if (message_to_send) {
            send_message(message_to_send);
            chatInputField.value = '';
        }
    }    
    // We can either send to the server if we press enter, or if we click the 'send' button.
    chatInputField.addEventListener('keypress', function (e) {
        // We don't care about other keys being clicked, so we just return early if the key pressed wasn't 'Enter'.
        if (e.key !== 'Enter') { 
            return;
        }
        process_send_event(e); 
    });
    sendButton.addEventListener('click', process_send_event);

    // --- CLIENT SIDE WEBSOCKET LOGIC ---
    let websocket;
    function connectToServer() {
        websocket = new WebSocket('wss://signallite.io/api/chatConnect');
        // Event listener for when the connection is opened
        websocket.addEventListener('open', (event) => {
            console.log('Connected to the WebSocket server.');
        });
        // Event listener for receiving messages
        websocket.addEventListener('message', (event) => {
            receive_message(event.data);
        });
        // Event listener for when the connection is closed
        websocket.addEventListener('close', (event) => {
            console.log('Disconnected from the WebSocket server.');
        });
        // Event listener for error handling
        websocket.addEventListener('error', (error) => {
            console.error('WebSocket error:', error);
        });
    }
    
    // Function to send data over the WebSocket connection
    function send_message(message) {
        console.log(message);
        if (websocket && websocket.readyState === WebSocket.OPEN) {
            websocket.send(message);
            console.log('Data sent:', message);
        } else {
            console.log('WebSocket is not open. Cannot send data.');
        }
    }
    // Function to handle receiving data from the WebSocket connection
    function receive_message(data) {
        // Parse the received data from JSON format
        let messageObject;
        try {
            messageObject = JSON.parse(data);
        } catch (error) {
            console.error("Failed to parse message data:", error);
            return;
        }
        // If the message is a LocalClient (sent to identify this client)
        if ('local_client_user_id' in messageObject) {
            // Store the user information for this client
            window.localClient = {
                user_id: messageObject.local_client_user_id,
            };
            console.log("Local client information received:", window.localClient);

        } else if ('user_id' in messageObject && 'message' in messageObject && 'timestamp' in messageObject) {
            const { user_id, message, timestamp } = messageObject;
            if(message == ""){
                return;
            }
            const isUser = window.localClient && window.localClient.user_id === user_id;
            createMessageBubble(message, isUser, timestamp);
        } else {
            console.warn("Unknown message format received:", messageObject);
        }
    }

    // --- CLIENT SIDE MESSAGE BUBBLE HELPERS ----
    // Used for creating the message bubbles we see on screen.

    // @author - ChatGPT.
    // Tells us the relative time in EST based on the UNIX timestamp told to us by the server.
    function getRelativeTime(timestamp) {
        if (typeof timestamp === 'string' || timestamp.toString().includes('.')) {
            timestamp = parseFloat(timestamp) * 1000;
        } else if (timestamp.toString().length === 10) {
            timestamp = timestamp * 1000; 
        }
        const messageTime = new Date(timestamp);
        const options = {
            timeZone: 'America/New_York',
            hour: 'numeric',
            minute: 'numeric',
            hour12: true;
        };
        return messageTime.toLocaleTimeString('en-US', options);
    }
    // Creates a message bubble based on received data.
    function createMessageBubble(messageText, isLocalClient, timestamp) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        // If it's a user message, add the 'user' class for the right-side alignment
        if (isLocalClient) {
            messageDiv.classList.add('user');
        }
        // Create the message bubble
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble');
        messageBubble.textContent = messageText;
        // Create the message info (for timestamp next to the bubble)
        const messageInfo = document.createElement('div');
        messageInfo.classList.add('message-info');
        // Add the relative time
        const timeElement = document.createElement('span');
        timeElement.classList.add('message-time');
        timeElement.textContent = getRelativeTime(timestamp);
        messageInfo.appendChild(timeElement);
        // Append the bubble and time to the main message div
        messageDiv.appendChild(messageBubble);
        messageDiv.appendChild(messageInfo);
        // Add the message to the chat container
        const chatMessages = document.querySelector('.chat-messages');
        chatMessages.appendChild(messageDiv);
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    // As soon as this page loads, establish websocket connection right away.
    connectToServer();
}

window.addEventListener("load", onLoaded);