document.addEventListener("DOMContentLoaded", () => {
    chrome.storage.local.get(["meanToxicity", "maxToxicity"], (data) => {
        document.getElementById("meanScore").innerText = data.meanToxicity ?? "N/A";
        document.getElementById("maxScore").innerText = data.maxToxicity ?? "N/A";
    });
}); 