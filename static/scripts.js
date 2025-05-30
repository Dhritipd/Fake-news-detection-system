document.addEventListener("DOMContentLoaded", function () {
    let data = JSON.parse(localStorage.getItem("newsResult"));

    if (!data) return;

    let newsStatus = document.getElementById("news-status");
    let confidenceBar = document.getElementById("confidence-bar");
    let confidenceScore = document.getElementById("confidence-score");
    let analysisExplanation = document.getElementById("analysis-explanation");

    newsStatus.innerHTML = data.is_fake ? "❌ Fake News Detected" : "✅ Likely Real News";
    newsStatus.style.color = data.is_fake ? "red" : "green";

    confidenceBar.style.width = data.confidence + "%";
    confidenceScore.innerText = `${data.confidence}% (${data.confidence > 70 ? "High" : "Low"})`;

    // Analysis Explanation
    analysisExplanation.innerHTML = data.confidence > 70 ? 
        "The confidence score is high, indicating strong classification." :
        "This content shows mixed signals. Please cross-check with trusted sources.";

    // Feature Analysis Chart
    const featureData = [
        data.features.source_credibility,
        data.features.clickbait_score,
        data.features.emotional_tone,
        data.features.expert_citations,
        data.features.factual_density
    ];
    
    new Chart(document.getElementById("featureChart").getContext("2d"), {
        type: "horizontalBar",
        data: {
            labels: ["Source Credibility", "Clickbait Score", "Emotional Tone", "Expert Citations", "Factual Density"],
            datasets: [{
                label: "Score (%)",
                data: featureData,
                backgroundColor: "blue",
            }]
        }
    });

    // Toggle Analysis
    document.getElementById("toggle-analysis").addEventListener("click", function () {
        let analysisSection = document.getElementById("feature-analysis");
        if (analysisSection.classList.contains("hidden")) {
            analysisSection.classList.remove("hidden");
            this.innerText = "Hide Content Feature Analysis ▲";
        } else {
            analysisSection.classList.add("hidden");
            this.innerText = "Show Content Feature Analysis ▼";
        }
    });
});
