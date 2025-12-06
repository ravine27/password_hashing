async function generate() {
    const password = document.getElementById("password").value;

    const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
    });

    const data = await res.json();

    const out = document.getElementById("results");
    out.innerHTML = "";

    for (let key in data) {
        out.innerHTML += `
            <div class="output-box">
                <h3>${key}</h3>
                <p><b>Hash:</b> ${data[key].hash}</p>
                ${data[key].salt ? `<p><b>Salt:</b> ${data[key].salt}</p>` : ""}
            </div>
        `;
    }
}
