// connect to WebSocket server
const socket = io();

// extract HTML elements
const messageList = document.getElementById('messages');
const message = document.getElementById('entered-message');
const globalMessageList = document.getElementById('global-messages');
const globalMessage = document.getElementById('global-entered-message');
const sendButton = document.getElementById('send-btn');
const globalSendBtn = document.getElementById('global-send-btn');
const chatName = document.getElementById('chat-name');
const searchInput = document.getElementById('search-contact')
const contactItems = document.getElementsByClassName('contact-item');
const modal = document.getElementById('new-msg-modal');
const addContactBtn = document.getElementById('add-contact-btn');
const closeModalBtn = document.getElementById('close-modal-btn');
const globalSearchInput = document.getElementById('global-search-input');
const globalSearchResults = document.getElementById('global-search-results');
const activeContactsList = document.getElementById('active-contacts-list');
const chatContainer = document.getElementById('chat-container')
const currentUserId = chatContainer.getAttribute('data-user-id');
const globalChatBtn = document.getElementById('global-chat-btn');
const privateChatBtn = document.getElementById('pvt-chat-btn');
const addNewContactBtn = document.getElementById("add-new-contact-btn")

// chat window regions/areas
const globalChatArea = document.getElementById('global-chat-area');
const privateChatArea = document.getElementById('private-chat-area');
const sidebar = document.getElementById('contact-sidebar');

const chatTypeHeader = document.getElementById('select-chat-type-header');

// selecting global vs private chat options
globalChatBtn.addEventListener('click', () => {
    if (chatTypeHeader)
        chatTypeHeader.style.display = 'none';
    privateChatArea.classList.remove('active');
    sidebar.classList.remove('active');
    globalChatArea.classList.add('active');
});

privateChatBtn.addEventListener('click', () => {
    if (chatTypeHeader)
        chatTypeHeader.style.display = 'none';
    globalChatArea.classList.remove('active');
    sidebar.classList.add('active');
    privateChatArea.classList.add('active');
});

// Global variable to track who you are talking to
let activeRecipientID = null;

// select a user to chat with
function chatWith(friendID, friendName) {
    activeRecipientID = friendID;
    chatName.innerText = friendName;
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
                listItem.classList.add('message-bubble');   // msg box shape

                if (msg.sender_name !== friendName) {
                    listItem.textContent = msg.message_content;
                    listItem.classList.add('sent');
                }
                else {
                    listItem.textContent = msg.message_content;
                    listItem.classList.add('received');
                }
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
    message.value = '';   // empty the message box

    if (textMsg.trim() !== "" && activeRecipientID !== null) {      // ono-to-one chat

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
// --- Fixed Contact Search ---
searchInput.addEventListener('input', () => {
    const userInput = searchInput.value.toLowerCase().trim();
    
    // Convert HTMLCollection to Array to ensure stable looping
    Array.from(contactItems).forEach(item => {
        // This gets all text inside the contact item (First Name, Last Name, etc.)
        const contactName = item.textContent.toLowerCase();

        if (contactName.includes(userInput)) {
            item.style.setProperty('display', 'flex', 'important'); 
        } else {
            item.style.setProperty('display', 'none', 'important');
        }
    });
});

// when user gets a message from the server,
socket.on('receive_private_message', (data) => {
    const msgBox = document.createElement('li');     // create a list item
    msgBox.classList.add('message-bubble');

    if (data.sender_id === Number(activeRecipientID)) {
        let currentFriendName = chatName.innerText;
        msgBox.textContent = currentFriendName + ': ' + data.text;
        msgBox.classList.add('received');
    }
    else {
        msgBox.textContent = data.text;
        msgBox.classList.add('sent');
    }

    messageList.appendChild(msgBox);
    document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;
});

// new user add and close btns
addContactBtn.addEventListener('click', () => { 
    modal.style.display = 'flex';
});
closeModalBtn.addEventListener('click', () => modal.style.display = 'none');

// searching global DB to add a new contact
globalSearchInput.addEventListener('input', () => {
    const contactSearched = globalSearchInput.value;

    // fetch the searched contact from the API
    fetch(`/api/search_db?q=${contactSearched}`).then(result => result.json())
        .then(data => {
            globalSearchResults.innerHTML = '';

            data.users.forEach(user => {
                const li = document.createElement('li');
                li.style.padding = '10px';
                li.style.display = 'flex';
                li.style.justifyContent = 'space-between';
                li.style.borderBottom = '1px solid #eee';

                li.innerHTML = `
                <span>${user.name}</span>
                <button class="brand-btn" style="padding: 5px 10px;">Add</button>`;

                // on clicking Add button
                const addBtn = li.querySelector('button');
                addBtn.addEventListener('click', () => {
                    // close the popup window
                    modal.style.display = 'none';

                    // add new contact to sidebar
                    const newContactLi = document.createElement('li');
                    newContactLi.className = 'contact-item';
                    newContactLi.textContent = user.name;
                    newContactLi.onclick = () => chatWith(user.id, user.name);
                    activeContactsList.append(newContactLi);

                    // start chatting
                    chatWith(user.id, user.name);
                });
            });
        });
});

// global message
globalSendBtn.addEventListener('click', () => {
    const msg = globalMessage.value;
    globalMessage.value = '';

    if (msg.trim() !== "") {
        socket.emit('send_global_message', {
            text: msg,
            sender_id: currentUserId
        })
    }
});

socket.on('receive_global_message', (data) => {
    const li = document.createElement('li');
    li.classList.add('message-bubble');

    if (data.sender_id == currentUserId)
    {
        li.classList.add('sent');
        li.innerHTML = `${data.text}`;
    }
    else
    {
        li.classList.add('received');
        li.innerHTML = `
            <span style="font-size: 0.8em; color: #555; display: block; margin-bottom: 4px; font-weight: bold;">
                ${data.sender}
            </span>
            ${data.text}
        `;
    }
    globalMessageList.appendChild(li);
    
    const globalChatWindow = document.getElementById('global-chat-window');
    if (globalChatWindow) {
        globalChatWindow.scrollTop = globalChatWindow.scrollHeight;
    }
});

// Listener for Private Chat Enter Key
message.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});

// Listener for Global Chat Enter Key
globalMessage.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        globalSendBtn.click();
    }
});


