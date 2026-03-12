// connect to WebSocket server
const socket = io();

// extract HTML elements
const messageList = document.getElementById('messages');
const message = document.getElementById('entered-message');
const sendButton = document.getElementById('send-btn');
const chatName = document.getElementById('chat-name');
const searchInput = document.getElementById('search-contact')
const contactItems = document.getElementsByClassName('contact-item')

// Global variable to track who you are talking to
let activeRecipientID = null;

// select a user to chat with
function chatWith(friendID, friendName) {
    activeRecipientID = friendID;
    chatName.innerText = 'Chatting with ' + friendName;
    messageList.innerText = '';

    // fetch and load the previous messages in a chat from the API in Flask 
    fetch(`/api/messages/${activeRecipientID}`)
        .then(response => {
            if (response.ok)
                return response.json();             // convert the API response to a JSON object
            else
                throw new Error("network response was not ok");
        })
        .then(data => {
            // loop thru the data and render it on the screen
            data.messages.forEach(msg => {
                const listItem = document.createElement('li');
                if (msg.sender_name !== friendName)
                    listItem.textContent = 'You: ' + msg.message_content;
                else
                    listItem.textContent = msg.sender_name + ': ' + msg.message_content;
                messageList.append(listItem);
            });
            // auto scroll to bottom of the screen
            document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;
        })
        .catch(error => {
            console.error(`DEBUG: Failed to load previous messages with ${friendName}`, error);
        });

    // join the chat room with friend after loading previous chats
    socket.emit('join_private_chat', { 'friend_id': activeRecipientID });
}

// when user clicks send,
sendButton.addEventListener('click', () => {
    const textMsg = message.value;
    message.textContent = '';

    if (textMsg.trim() !== "" && activeRecipientID !== null) {

        // emit the message to backend server
        socket.emit('send_private_message', {
            'text': textMsg,
            'friend_id': activeRecipientID
        });

        message.value = '';     // clear the input box for a new message to be entered
    }
    else if (activeRecipientID == null) {
        alert("Select a user to chat with!");
    }
});


//Listen for the search event
searchInput.addEventListener('input', ()=>{
    const userInput = searchInput.value.toLowerCase();
    for (let i = 0; i < contactItems.length; i++) {
        let currentContact = contactItems[i];
        let contactName = currentContact.textContent.toLowerCase();

        if (contactName.includes(userInput))
            currentContact.style.display = "";
        else
            currentContact.style.display = "none";
    }
});

// when user gets a message from the server,
socket.on('receive_private_message', (data) => {
    const msgBox = document.createElement('li');     // create a list item
    if (data.sender_id === Number(activeRecipientID)) {
        let currentFriendName = chatName.innerHTML.replace('Chatting with ', '');
        msgBox.textContent = currentFriendName + ': ' + data.text;
    }
    else {
        msgBox.textContent = 'You: ' + data.text;
    }
    messageList.appendChild(msgBox);
    // auto scroll to bottom of the message screen
    document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;
});