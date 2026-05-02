const chatBody = document.getElementById("chatBody");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendChatBtn")

// Handle back and fourth messaging 
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

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        const reply = typeof data.reply === "string" ? data.reply.trim() : "";

        if (!res.ok || !reply) {
            console.error(data.error || "Empty tutor reply");
            return;
        }

        appendMessage(reply, "bot");
    } catch (error) {
        console.error("Chat request failed", error);
    }
}

sendBtn.addEventListener("click", sendMessage);

// This does not work, <textarea> should automatically also add a newline. 
// So do some due dilligence on <textarea>.
userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        userInput.value += "\n";
    }
});
// Back and fourth message handling end

// Set the current objective 
async function setObjective(objective) {
    const res = await fetch("/set_objective", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ objective })
    });

    const data = await res.json();

    if (!res.ok) {
        console.error(data.error || "Mode setting failed");
        return;
    }

    if (data.ready) {
        const prompt = document.getElementById("objectivePrompt");
        if (prompt) prompt.remove();

        appendMessage(`Objective set: ${data.objective}. Let's get to work`, "assistant");
    }
}

// Get the objective via button click events
function showObjectivePrompt() {
    const wrapper = document.createElement("div")
    wrapper.id = "objectivePrompt"
    wrapper.className = "assistant-message objective-prompt"

    wrapper.innerHTML = `
      <p>What are we working on today?</p>
        <div class="objective-buttons">
           <button data-objective="studying">Studying</button>
           <button data-objective="school_work">School Work</button>
        </div>
      `;
    
    chatBody.appendChild(wrapper);

    wrapper.querySelectorAll("button").forEach(button => {
        button.addEventListener("click", async () => {
            const objective = button.dataset.objective;
            await setObjective(objective)
        });
    });
}
showObjectivePrompt()

