// Fetch data from Flask API
async function loadResults() {
    const res = await fetch("http://127.0.0.1:5000/results");
    const data = await res.json();

    populateTable(data);
    renderCharts(data);
}

// Populate the results table
function populateTable(results) {
    const tbody = document.querySelector("#resultsTable tbody");
    tbody.innerHTML = "";

    results.forEach(row => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${row.id}</td>
            <td>${row.type}</td>
            <td>${row.input_text || "-"}</td>
            <td>${row.filename || "-"}</td>
            <td>${row.verdict}</td>
            <td>${row.explanation}</td>
            <td>${row.timestamp}</td>
        `;

        tbody.appendChild(tr);
    });
}

// Render pie & bar charts
function renderCharts(results) {
    const humanCount = results.filter(r => r.verdict.includes("Human")).length;
    const aiCount = results.filter(r => r.verdict.includes("AI")).length;

    const textCount = results.filter(r => r.type === "text").length;
    const imageCount = results.filter(r => r.type === "image").length;

    // PIE CHART: Human vs AI
    new Chart(document.getElementById("aiPieChart"), {
        type: "pie",
        data: {
            labels: ["Human", "AI"],
            datasets: [{
                data: [humanCount, aiCount],
                backgroundColor: ["#4CAF50", "#FF5252"]
            }]
        }
    });

    // BAR CHART: Text vs Image
    new Chart(document.getElementById("typeBarChart"), {
        type: "bar",
        data: {
            labels: ["Text Analyses", "Image Analyses"],
            datasets: [{
                label: "Count",
                data: [textCount, imageCount],
                backgroundColor: ["#2196F3", "#9C27B0"]
            }]
        }
    });
}

// Initialize dashboard
loadResults();
