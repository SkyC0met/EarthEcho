class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        console.log('openButton:', this.args.openButton);
        console.log('chatBox:', this.args.chatBox);
        console.log('sendButton:', this.args.sendButton);

        this.state = false;  // chatbot is closed initially
        this.messages = [];  // store messages
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        // Listen for Enter key press in input field
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        // Toggle the value of the 'state' property (true to false, false to true)
        this.state = !this.state;

        // Show or hide the chatbox
        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input'); // Extract user input
        let text1 = textField.value.trim();
        // Check if user input is empty
        if (text1 === "") {
            return;
        }

        // Sanitize user input using 'he' library for HTML encoding
        let sanitizedText = he.encode(text1);

        let msg1 = { name: "User", message: sanitizedText }; // Object for user input
        this.messages.push(msg1); // Add to messages array

        // Send sanitized text to server for processing
        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: sanitizedText }),
            // Cross-Origin Resource Sharing
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Include CSRF token
            },
        })
        .then(r => r.json())
        .then(r => {
            // Sanitize chatbot response before displaying
            let sanitizedResponse = he.encode(r.answer);
            let msg2 = { name: "Greeny", message: sanitizedResponse }; // Object for chatbot response
            this.messages.push(msg2); // Add to messages array
            this.updateChatText(chatbox);
            textField.value = ''; // Clear input field after sending message
        })
        .catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
            textField.value = '';
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item) {
            if (item.name === "Greeny") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        // Update chatbox messages container with the generated HTML
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const chatbox = new Chatbox();
    chatbox.display();
});
