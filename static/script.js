const passwordInput = document.getElementById("password");

if (passwordInput) {
  passwordInput.addEventListener("input", function () {
    const password = passwordInput.value;

    fetch("/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
      const strengthEl = document.getElementById("strength");
      const bar = document.getElementById("strength-bar");
      const suggestionsList = document.getElementById("suggestions-list");
      const historyWarning = document.getElementById("history-warning");

      strengthEl.textContent = `Strength: ${data.strength}`;
      suggestionsList.innerHTML = "";
      data.suggestions.forEach(text => {
        const li = document.createElement("li");
        li.textContent = text;
        suggestionsList.appendChild(li);
      });

      historyWarning.textContent = data.remarks.length > 0 ? data.remarks[0] : "";

      // Update bar style
      if (data.strength === "Weak") {
        bar.style.width = "30%";
        bar.style.backgroundColor = "red";
        strengthEl.style.color = "red";
      } else if (data.strength === "Moderate") {
        bar.style.width = "60%";
        bar.style.backgroundColor = "orange";
        strengthEl.style.color = "orange";
      } else if (data.strength === "Strong") {
        bar.style.width = "100%";
        bar.style.backgroundColor = "green";
        strengthEl.style.color = "green";
      }
    });
  });
}
function togglePassword(inputId) {
    const passwordInput = document.getElementById(inputId);
    if (passwordInput) {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
        } else {
            passwordInput.type = "password";
        }
    }
}
