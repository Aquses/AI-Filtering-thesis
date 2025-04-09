document.addEventListener("DOMContentLoaded", () => {
    let textContent = document.body ? document.body.innerText : "";

    // function checkImgBySize(img) {
    //     return img.naturalWidth <= 64 || img.naturalHeight <= 64;
    // }

    let images = [...document.images]
        .map(img => img.src)
        .filter(src => /\.(jpeg|jpg|png|webp)$/i.test(src) && !/(icon|icons|favicon|data:image|svg)/i.test(src));

    const sentences = textContent.split(/[.!?]\s/).map(sentence => sentence.trim()).filter(Boolean);
    const cleanedSentences = sentences.filter(sentence => !/\b(icon|icons|favicon)\b/i.test(sentence));

    let combinedSentences = [];
    let currentSentence = [];
    let currentWordCount = 0;

    cleanedSentences.forEach(sentence => {
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
