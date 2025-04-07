document.addEventListener("DOMContentLoaded", () => {
    let textContent = document.body ? document.body.innerText : "";
    let images = [...document.images]
        .map(img => img.src)
        .filter(src => /\.(jpeg|jpg|png|webp)$/i.test(src));
    
    
    const sentences = textContent.split(/[.!?]\s/).map(sentence => sentence.trim()).filter(Boolean);
    
    let combinedSentences = [];
    let currentSentence = [];
    let currentWordCount = 0;

    sentences.forEach(sentence => {
        let wordCount = sentence.split(' ').length;
        
        if (currentWordCount + wordCount <= 35) {
            currentSentence.push(sentence);
            currentWordCount += wordCount;
        } else {
            combinedSentences.push(currentSentence.join(' '));
            currentSentence = [sentence];
            currentWordCount = wordCount;
        }
    });
    images.forEach(imageUrl => {
        chrome.runtime.sendMessage({
            type: 'analyze_image',
            image: imageUrl
        }, (response) => {
            console.log('Image analysis result:', response);
        });
    });

    if (currentSentence.length > 0) {
        combinedSentences.push(currentSentence.join(' '));
    }

    console.log(images)
    console.log("Sentences:", combinedSentences);
    
    chrome.runtime.sendMessage({ type: 'check_explicit_content', text: textContent });
});
