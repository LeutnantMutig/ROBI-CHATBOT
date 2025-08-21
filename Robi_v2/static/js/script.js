const chatMessages = document.querySelector('.chat-messages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
// const currentTimeElement = document.getElementById('currentTime');

// Update current time every second
// setInterval(updateCurrentTime, 1000);

// sendButton.addEventListener('click', sendMessage);
function sendMessage() {
  const userMessage = userInput.value.trim();
  if (userMessage) {
    displayMessage(userMessage, 'user');
    userInput.value = '';

    // Call your ChatGPT integration code here
    getChatGPTResponse(userMessage)
      .then(response => {
        displayMessage(response, 'bot');
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
}

function displayMessage(message, sender) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', `${sender}-message`);

  const iconElement = document.createElement('div');
  iconElement.classList.add('message-icon');
  iconElement.textContent = sender === 'user' ? '👤' : '👻';

  const textElement = document.createElement('p');
  textElement.classList.add('message-text');
  textElement.textContent = message;

  messageElement.appendChild(iconElement);
  messageElement.appendChild(textElement);

  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getChatGPTResponse(message) {
  // Replace this with your actual code to communicate with ChatGPT
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve('This is a sample response from ChatGPT.');
    }, 1000);
  });
}

// function updateCurrentTime() {
//   const now = new Date();
//   const hours = now.getHours().toString().padStart(2, '0');
//   const minutes = now.getMinutes().toString().padStart(2, '0');
//   const currentTime = `${hours}:${minutes}`;
//   currentTimeElement.textContent = currentTime;
// }