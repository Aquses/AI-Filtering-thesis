const MIN_WIDTH = 64;
const MIN_HEIGHT = 64;
const MIN_ASPECT_RATIO = 1.2;

function checkImgBySize({ naturalWidth: width, naturalHeight: height }) {
    if (width <= MIN_WIDTH || height <= MIN_HEIGHT) return false;
    const aspectRatio = width / height;
    return aspectRatio >= MIN_ASPECT_RATIO;
}

function processSentences(text) {
    const sentences = text.split(/[.!?]\s/)
        .map(sentence => sentence.trim())
        .filter(Boolean);

    const cleanedSentences = sentences.filter(sentence => !/\b(icon|icons|favicon)\b/i.test(sentence));

    const combinedSentences = [];
    let currentSentence = [];
    let currentWordCount = 0;

    cleanedSentences.forEach(sentence => {
        const wordCount = sentence.split(' ').length;

        if (currentWordCount + wordCount <= 35) {
            currentSentence.push(sentence);
            currentWordCount += wordCount;
        } else {
            combinedSentences.push(currentSentence.join(' '));
            currentSentence = [sentence];
            currentWordCount = wordCount;
        }
    });

    if (currentSentence.length > 0) {
        combinedSentences.push(currentSentence.join(' '));
    }
    return combinedSentences;
}

function getValidImages() {
    return [...document.images]
        .map(({ src }) => src)
        .filter(src => /\.(jpeg|jpg|png|webp)$/i.test(src) && !/(icon|icons|favicon|data:image|svg)/i.test(src));
}

document.addEventListener("DOMContentLoaded", async () => {
    const textContent = document.body?.innerText || '';
    const combinedSentences = processSentences(textContent);
    const images = getValidImages();

    console.log('Valid images:', images);
    console.log('Sentences:', combinedSentences);

    chrome.runtime.sendMessage({
        type: 'check_explicit_content',
        text: textContent
    });

    await Promise.all(images.map(async (imageUrl) => {
        const img = new Image();
        img.src = imageUrl;

        await new Promise((resolve, reject) => {
            img.onload = resolve;
            img.onerror = reject;
        });

        if (checkImgBySize(img)) {
            chrome.runtime.sendMessage({
                type: 'analyze_image',
                image: imageUrl
            }, (response) => {
                console.log('Image analysis result:', response);
            });
        }
    }));
});
