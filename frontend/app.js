let score = 0;

async function submitGuess() {
  const seed = document.getElementById("seed").value.trim();
  const guess = document.getElementById("guess").value.trim();
  const resultDiv = document.getElementById("result");

  if (!seed || !guess) {
    resultDiv.innerHTML = "Please enter both seed and guess.";
    return;
  }

  const response = await fetch("http://127.0.0.1:8000/guess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ seed: seed, guess: guess })
  });

  const data = await response.json();
  console.log("API Response:", data); // 🧪 Show full response in console

  if (data.result === "Game Over") {
    resultDiv.innerHTML = `<b>❌ Game Over:</b> ${data.reason}`;
    score = 0;
  } else if (data.result === "Wrong Guess") {
    resultDiv.innerHTML = `<b>❌</b> ${data.message}`;
  } else if (data.result === "Correct Guess") {
    resultDiv.innerHTML = `<b>✅ Correct!</b><br>${JSON.stringify(data)}`;
    score = data.current_score || 0;
  } else {
    resultDiv.innerHTML = "Something went wrong.";
  }

  document.getElementById("score").innerText = `Score: ${score}`;
  document.getElementById("history").innerText =
    "History: " + (data.guess_history || []).join(", ");
}
