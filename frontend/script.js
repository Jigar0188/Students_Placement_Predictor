const form = document.getElementById("prediction-form");
const predictBtn = document.getElementById("predict-btn");
const statusText = document.getElementById("status");
const resultSection = document.getElementById("result");
const resultTitle = document.getElementById("result-title");
const resultProbability = document.getElementById("result-probability");

// FastAPI endpoint
const API_URL = "http://127.0.0.1:8000/predict";

form.addEventListener("submit", async function (event) {
  // Prevent page reload
  event.preventDefault();

  // Hide previous result
  resultSection.hidden = true;
  statusText.textContent = "Generating prediction...";
  predictBtn.disabled = true;

  try {
    // Collect all form values
    const formData = new FormData(form);
    const student = Object.fromEntries(formData.entries());

    // Convert numeric strings into numbers
    const numericFields = [
      "attendance_percent",
      "communication_skill",
      "tech_events_attended",
      "salary_expectation",
      "cgpa",
      "coding_problems_solved",
    ];

    for (const field of numericFields) {
      student[field] = Number(student[field]);
    }

    // Send data to FastAPI
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(student),
    });

    // Handle API errors
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail
          ? JSON.stringify(errorData.detail)
          : "Prediction request failed.",
      );
    }

    // Read prediction response
    const data = await response.json();

    // Display result
    resultTitle.textContent = data.result;
    resultProbability.textContent = `Placement probability: ${(data.probability * 100).toFixed(2)}%`;

    resultSection.hidden = false;
    statusText.textContent = "Prediction completed successfully!";
  } catch (error) {
    console.error("Prediction error:", error);
    statusText.textContent = `Error: ${error.message}. Check whether FastAPI is running.`;
  } finally {
    predictBtn.disabled = false;
  }
});
