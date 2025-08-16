const chatWrapper = document.querySelector('.chat-wrapper');

window.onload = function() {
    chatWrapper.scrollTop = chatWrapper.scrollHeight;
}


let selected_user = document.getElementById('selected_user').innerText +"/"

if (selected_user==="/"){
    selected_user=""
}
console.log(selected_user)

const chatSocket = new WebSocket(
    "ws://127.0.0.1:8000/ws/chat/"+selected_user
    )

const chatHistory = document.querySelector('.chat-history');

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data.text;
    console.log("add a div on message");

    const newDiv = document.createElement('div');
    newDiv.className = 'message';

    const usernameElement = document.createElement('i');
    usernameElement.textContent = data.from_who;

    const contentElement = document.createElement('span');
    contentElement.textContent = message;

    newDiv.appendChild(usernameElement);
    newDiv.appendChild(document.createTextNode(': '));
    newDiv.appendChild(contentElement);

    // Добавляем сообщение в историю чата
    chatHistory.prepend(newDiv);
};
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

let inputField = document.querySelector(".input-field");
let sendButton = document.querySelector(".button-sub");

function handleEnterKeyPress(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        if (inputField.value.trim() !== "") {
            sendButton.click();
        }
    }
}

function handleSendButtonClick() {
    if (inputField.value.trim() !== "") {
        chatSocket.send(JSON.stringify({
            'message': inputField.value
        }));
        console.log("send a message")
        inputField.value = "";
    }
}

inputField.addEventListener("keypress", handleEnterKeyPress);
sendButton.addEventListener("click", handleSendButtonClick);