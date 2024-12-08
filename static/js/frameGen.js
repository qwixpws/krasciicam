const frameDiv = document.getElementById('frame');
const iframe = document.getElementById('iframe');
const frameSpeed = 30;

async function fetchFrame() {
    const decoder = new TextDecoder();

    let done = false;
    let value;

    while (!done) {
        const response = await fetch('/vidfeed');
        const reader = response.body.getReader();
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const frame = decoder.decode(value, { stream: true });
        handleFrames(frame);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function handleFrames(data) {
    let frameCount = frameSpeed;
    frameLength = data.length / frameSpeed;
    let i = 0;

    while (frameCount > 0) {
        frame = data.slice(i, (i + frameLength));
        i += frameLength;
        frameCount--;
        frameDiv.innerHTML = frame;
        await sleep(1000 / frameSpeed);
    }
}

fetchFrame();
