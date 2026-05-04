// ============================================
// State Management
// ============================================

let currentUser = null;
let currentObjective = null;

// ============================================
// DOM Elements
// ============================================

const onboardingContainer = document.getElementById("onboardingContainer");
const chatContainer = document.getElementById("chatContainer");
const loadingIndicator = document.getElementById("loadingIndicator");

const onboardingForm = document.getElementById("onboardingForm");
const onboardingError = document.getElementById("onboardingError");

const chatBody = document.getElementById("chatBody");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendChatBtn");
const msgBox = document.getElementById("msgBox");
const welcomeTitle = document.getElementById("welcomeTitle");

// ============================================
// UI State Management
// ============================================

function showLoading() {
    loadingIndicator.style.display = "flex";
    onboardingContainer.style.display = "none";
    chatContainer.style.display = "none";
}

function showOnboarding() {
    loadingIndicator.style.display = "none";
    onboardingContainer.style.display = "flex";
    chatContainer.style.display = "none";
}

function showChat() {
    loadingIndicator.style.display = "none";
    onboardingContainer.style.display = "none";
    chatContainer.style.display = "flex";
}

function showError(message) {
    onboardingError.textContent = message;
    onboardingError.style.display = "block";
}

function hideError() {
    onboardingError.style.display = "none";
}

// ============================================
// API Calls
// ============================================

async function checkUserStatus() {
    try {
        const res = await fetch("/status", {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        
        const data = await res.json();
        
        if (data.logged_in) {
            currentUser = {
                name: data.user_name,
                age: data.user_age,
                skill_level: data.user_skill_level
            };
            return true;
        }
        return false;
    } catch (error) {
        console.error("Status check failed", error);
        return false;
    }
}

async function submitOnboarding(name, age, skillLevel) {
    try {
        const res = await fetch("/onboard", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: name,
                age: age,
                skill_level: skillLevel
            })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || "Onboarding failed");
        }

        currentUser = {
            name: data.user_name,
            age: age,
            skill_level: skillLevel
        };

        return true;
    } catch (error) {
        console.error("Onboarding submission failed", error);
        throw error;
    }
}

async function setObjective(objective) {
    try {
        const res = await fetch("/set_objective", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ objective: objective })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || "Objective setting failed");
        }

        if (data.ready) {
            currentObjective = data.objective;
            return true;
        }
        return false;
    } catch (error) {
        console.error("Set objective failed", error);
        throw error;
    }
}

async function sendChatMessage(message) {
    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || "Chat request failed");
        }

        return data.reply;
    } catch (error) {
        console.error("Chat request failed", error);
        throw error;
    }
}

// ============================================
// Chat UI Functions
// ============================================

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

async function handleSendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    try {
        const reply = await sendChatMessage(message);
        appendMessage(reply, "bot");
    } catch (error) {
        appendMessage("Sorry, something went wrong. Please try again.", "bot");
    }
}

function showObjectivePrompt() {
    const wrapper = document.createElement("div");
    wrapper.id = "objectivePrompt";
    wrapper.className = "assistant-message objective-prompt";

    wrapper.innerHTML = `
      <p>What are we working on today?</p>
      <div class="objective-buttons">
        <button data-objective="studying">Studying</button>
        <button data-objective="school_work">School Work</button>
      </div>
    `;

    msgBox.appendChild(wrapper);

    wrapper.querySelectorAll("button").forEach(button => {
        button.addEventListener("click", async () => {
            const objective = button.dataset.objective;
            try {
                await setObjective(objective);
                wrapper.remove();
                appendMessage(`Great! Let's focus on ${objective}. What can I help you with?`, "bot");
            } catch (error) {
                appendMessage("Sorry, something went wrong. Please try again.", "bot");
            }
        });
    });
}

// ============================================
// Onboarding Form Handling
// ============================================

onboardingForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideError();

    const name = document.getElementById("nameInput").value.trim();
    const age = document.getElementById("ageInput").value.trim();
    const skillLevel = document.getElementById("skillInput").value;

    if (!name || !age || !skillLevel) {
        showError("Please fill in all fields");
        return;
    }

    try {
        await submitOnboarding(name, age, skillLevel);
        
        // Clear form
        onboardingForm.reset();
        
        // Update UI
        welcomeTitle.textContent = `Welcome, ${name}`;
        msgBox.innerHTML = "";
        
        // Show chat and prompt for objective
        showChat();
        appendMessage("Great! Let's get started. What would you like to work on?", "bot");
        showObjectivePrompt();
    } catch (error) {
        showError(error.message);
    }
});

// ============================================
// Chat Event Listeners
// ============================================

sendBtn.addEventListener("click", handleSendMessage);

userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleSendMessage();
    }
});

// ============================================
// Page Initialization
// ============================================

async function initializePage() {
    showLoading();

    try {
        const isLoggedIn = await checkUserStatus();

        if (isLoggedIn && currentUser) {
            // User exists - show chat interface
            welcomeTitle.textContent = `Welcome, ${currentUser.name}`;
            msgBox.innerHTML = "";
            showChat();
            appendMessage("Welcome back! What can I help you with today?", "bot");
            showObjectivePrompt();
        } else {
            // No user - show onboarding
            showOnboarding();
        }
    } catch (error) {
        console.error("Initialization failed", error);
        showOnboarding();
    }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", initializePage);

