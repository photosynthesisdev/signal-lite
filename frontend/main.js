function onLoaded(event){

  const chatInputField = document.querySelector('.chat-input');
  const sendButton = document.querySelector('.chat-send-btn');
  const chatMessages = document.querySelector('.chat-messages');
  
  function process_send_event(e){
      e.preventDefault();
      const message_to_send = chatInputField.value.trim();
      if (message_to_send) {
          send_message(message_to_send);
          chatInputField.value = '';
      }
  }
  sendButton.addEventListener('click', process_send_event);
  
  // Trigger sending a message if the user pressed enter only.
  chatInputField.addEventListener('keypress', function (e) {
      // We don't care about other keys being clicked, so we just return early if the key pressed wasn't 'Enter'.
      if (e.key !== 'Enter') { 
        return;
      }
      process_send_event(e); 
  });
  
  // Function to create and append a new message bubble
  function createMessageBubble(messageText, isUser, senderName = "Anonymous") {
      // Create the main message div
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('message');
      // If it's a user message, add the 'user' class for the right-side alignment
      if (isUser) {
          messageDiv.classList.add('user');
      }
  
      // Create the message bubble
      const messageBubble = document.createElement('div');
      messageBubble.classList.add('message-bubble');
      messageBubble.textContent = messageText;
  
      // Create the message info (name and time)
      const messageInfo = document.createElement('div');
      messageInfo.classList.add('message-info');
  
      if (!isUser) {
          // Add sender's name for non-user messages (left-side)
          const nameElement = document.createElement('span');
          nameElement.classList.add('message-name');
          nameElement.textContent = senderName;
          messageInfo.appendChild(nameElement);
      }
  
      // Add timestamp
      // const timeElement = document.createElement('span');
      // timeElement.classList.add('message-time');
      // timeElement.textContent = getCurrentTime();
      // messageInfo.appendChild(timeElement);
  
      // Append the message info and bubble to the main message div
      messageDiv.appendChild(messageInfo);
      messageDiv.appendChild(messageBubble);
  
      // Add the message to the chat container
      chatMessages.appendChild(messageDiv);
  
      // Scroll to the bottom of the chat
      chatMessages.scrollTop = chatMessages.scrollHeight;
  }

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
  function send_message(data) {
      console.log(data);
      if (socket && socket.readyState === WebSocket.OPEN) {
          socket.send(data);
          console.log('Data sent:', data);
      } else {
          console.log('WebSocket is not open. Cannot send data.');
      }
  }
  // Function to handle receiving data from the WebSocket connection
  function receive_message(data) {
      console.log('Data received:', data);
  }
  connectToServer();
}

window.addEventListener("load", onLoaded);