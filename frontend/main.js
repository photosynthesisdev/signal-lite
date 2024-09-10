window.addEventListener("load", (event) => {

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
  
  // If we click the 'send button', process the send event.
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
  
  
  function send_message(message){
    // Sends a message to the server over the websocket connection. This is a new message we want to publish to the chat room.
  }
  
  function receive_message(message_object){
    // Receives some message json from the server.
    // Publishes it to the chat
  }
});