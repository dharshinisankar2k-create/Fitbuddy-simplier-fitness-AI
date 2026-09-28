// For local testing:
const API_URL = "http://127.0.0.1:5000";

// After deploying the backend, replace the line above with your Render URL.
// Example:
// const API_URL = "https://your-fitbuddy-backend.onrender.com";

const form = document.getElementById("fitnessForm");
const button = document.getElementById("generateBtn");
const statusBox = document.getElementById("status");
const resultCard = document.getElementById("resultCard");
const planBox = document.getElementById("plan");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const data = {
    age: document.getElementById("age").value,
    height: document.getElementById("height").value,
    weight: document.getElementById("weight").value,
    goal: document.getElementById("goal").value,
    fitness_level: document.getElementById("fitness_level").value
  };

  button.disabled = true;
  button.textContent = "Generating...";
  statusBox.textContent = "FitBuddy is creating your plan...";
  resultCard.classList.add("hidden");

  try {
    const response = await fetch(`${API_URL}/generate-plan`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Unable to generate plan.");
    }

    planBox.innerHTML = `<pre>${escapeHtml(result.plan)}</pre>`;
    resultCard.classList.remove("hidden");
    statusBox.textContent = "Your plan is ready!";
  } catch (error) {
    statusBox.textContent = error.message;
  } finally {
    button.disabled = false;
    button.textContent = "Generate My Plan";
  }
});

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
