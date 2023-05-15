chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  if (tabs && tabs.length > 0) {
    chrome.scripting.executeScript(
      {
        target: { tabId: tabs[0].id },
        function: () => {
          let tabText = document.body.innerText;
          chrome.runtime.sendMessage({ tabText: tabText });
        },
      },
      () => {
        console.error('Error executing script in tab');
      }
    );
  } else {
    console.error('Error getting active tab');
  }
});

const para = '';
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.tabText) {
    document.getElementById('tabText').textContent = request.tabText;
  }
});

// Get references to the chat box, message input, and Ask button
const chatbox = document.getElementById('chatbox');
const messageInput = document.getElementById('message');
const askButton = document.getElementById('ask');

// Add a click event listener to the Ask button
const typing = document.getElementById('typing');

askButton.addEventListener('click', () => {
  const message = messageInput.value;
  const paragraph = document.getElementById('tabText').textContent;
  const data = {
    question: message,
    paragraph: paragraph,
  };

  // Get the user's message

  if (message != '') {
    typing.style.display = 'block';

    // Disable the Ask button
    // const askButton = document.getElementById('ask');
    // askButton.disabled = true;

    // Append the user's message to the chat box
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('message', 'user-message');
    userMessageElement.innerHTML = `<strong>Question:</strong> ${message}`;
    chatbox.appendChild(userMessageElement);

    const chatbotMessageElementTemp = document.createElement('div');

    chatbotMessageElementTemp.classList.add('message', 'chatbot-message');
    const typingElement = document.createElement('typing');
    chatbotMessageElementTemp.innerHTML = `<strong>Answer:</strong> Loading...`;
    chatbox.appendChild(chatbotMessageElementTemp);

    // Send the user's message to the chatbot and get the response
    fetch('http://127.0.0.1:8080/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.answer);
        const responses = data.answer;
        const chatbotMessageElement = document.createElement('div');
        chatbox.removeChild(chatbox.lastChild);
        chatbotMessageElement.classList.add('message', 'chatbot-message');
        chatbotMessageElement.innerHTML = `<strong>Answer:</strong> ${responses}`;
        chatbox.appendChild(chatbotMessageElement);
        typing.style.display = 'none';
        // Clear the message input
        messageInput.value = '';
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        typing.style.display = 'none';
      });
  }
});

document
  .getElementById('ask-form')
  .addEventListener('submit', function (event) {
    event.preventDefault();
  });
