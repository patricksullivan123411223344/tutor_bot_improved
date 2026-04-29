const chatBody = document.getElementById("chatBody");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendChatBtn")

function appendMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message_box", sender);

    if (sender === "bot") {
        div.innerHTML = marked.parse(text);
    } else {
        div.textContent = text;
    }

    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user")
    userInput.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await res.json();
    appendMessage(data.reply, "bot");
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});