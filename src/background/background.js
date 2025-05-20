import { extractContentScore, isExplicitContent } from './analyzeHelpers.js';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'check_explicit_content') {
        checkTextForExplicitContent(request.text, sender.tab.id);
    }
    if (request.type === 'analyze_image') {
        const imageUrl = request.image;
        analyzeImageWithSightEngine(imageUrl, (data) => {
            sendResponse(data);
        });
        return true;
    }
});

function checkTextForExplicitContent(text, tabId) {
    const API_KEY = import.meta.env.VITE_API_KEY_PRIMITIVE_AI;
    const url = `https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=${API_KEY}`;

    const sentences = text.split(/[.!?]\s+/).map(sentence => sentence.trim()).filter(Boolean);

    let sentencePromises = sentences.map(sentence => {
        let payload = {
            comment: { text: sentence },
            languages: ["en"],
            requestedAttributes: {
                TOXICITY: {},
                SEVERE_TOXICITY: {},
                INSULT: {},
                PROFANITY: {},
                THREAT: {},
                SPAM: {}
            }
        };

        return fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                return {
                    text: sentence,
                    toxicity: data.attributeScores?.TOXICITY?.summaryScore?.value || 0
                };
            })
            .catch(error => {
                console.error("API Error:", error);
                return { text: sentence, toxicity: 0 };
            });
    });

    Promise.all(sentencePromises).then(results => {
        let highestScoringSentences = results.sort((a, b) => b.toxicity - a.toxicity).slice(0, 5);
        let meanToxicity = results.reduce((sum, r) => sum + r.toxicity, 0) / results.length;
        let highestToxicity = highestScoringSentences[0]?.toxicity || 0;

        let THRESHOLD_HIGH = 0.8;
        let THRESHOLD_MEAN = 0.5;

        let shouldBlock = highestToxicity >= THRESHOLD_HIGH ||
            highestScoringSentences.reduce((sum, s) => sum + s.toxicity, 0) / highestScoringSentences.length >= THRESHOLD_MEAN;

        console.log(highestScoringSentences)
        console.log(highestScoringSentences.reduce((sum, s) => sum + s.toxicity, 0) / highestScoringSentences.length)
        console.log(highestToxicity)
        chrome.storage.local.set({
            meanToxicity: meanToxicity.toFixed(2),
            maxToxicity: highestToxicity.toFixed(2),
        });
        if (shouldBlock) {
            chrome.tabs.update(tabId, { url: chrome.runtime.getURL("blockedPage/blocked.html") });
        }
    });
}

function analyzeImageWithSightEngine(imageUrl) {
    const API_USER = import.meta.env.VITE_API_USER_SIGHT_ENGINE;
    const API_SECRET = import.meta.env.VITE_API_SECRET_SIGHT_ENGINE;
    const API_URL = 'https://api.sightengine.com/1.0/check.json';

    console.log(`Analyzing image: ${imageUrl}`);

    const params = new URLSearchParams({
        url: imageUrl,
        models: 'nudity-2.1,weapon,alcohol,recreational_drug,medical,offensive-2.0,face-attributes,gore-2.0,violence,self-harm',
        api_user: API_USER,
        api_secret: API_SECRET
    });

    fetch(`${API_URL}?${params.toString()}`, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            console.log('API Response:', JSON.stringify(data, null, 2));
            if (!data || data.status !== 'success') {
                console.error('Invalid API response:', data);
                return;
            }

            const scores = extractContentScore(data);
            console.log('Extracted Scores:', scores);

            const customThresholds = {
                sexual_activity: 0.5,
                erotica: 0.5,
                firearm: 0.5,
                alcohol: 0.5,
                drugs: 0.5,
                offensive: 0.5,
                gore: 0.5,
                violence: 0.5,
                selfharm: 0.5
            };

            const isExplicit = isExplicitContent(scores, customThresholds);
            console.log('Explicit content detected?', isExplicit);

            if (isExplicit) {
                console.log('Sending message to content script to blur image.');
                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    if (tabs.length === 0) {
                        console.error('No active tab found.');
                        return;
                    }
                    chrome.scripting.executeScript({
                        target: { tabId: tabs[0].id },
                        function: blurExplicitImage,
                        args: [imageUrl]
                    });
                });
            } else {
                console.log('Image is safe.');
            }
        })
        .catch(error => {
            console.error('Error calling SightEngine API:', error);
        });
}

function blurExplicitImage(imageUrl) {
    document.querySelectorAll('img').forEach(img => {
        const imgSrcs = [img.src, img.getAttribute('data-src'), img.currentSrc];

        if (imgSrcs.includes(imageUrl)) {
            img.style.filter = 'blur(20px)';
            img.style.transition = 'filter 0.3s ease-in-out';
        }
    });
}
