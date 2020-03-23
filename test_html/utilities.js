const videoWidth = 600;
const videoHeight = 500;
var x = false;

document.addEventListener('DOMContentLoaded',domloaded,false);

async function setupCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error(
            'Browser API navigator.mediaDevices.getUserMedia not available');
    }

    const video = document.getElementById('video');
    video.width = videoWidth;
    video.height = videoHeight;

    video.srcObject = await navigator.mediaDevices.getUserMedia({
        'audio': false,
        'video': {
            facingMode: 'user',
            width: videoWidth,
            height: videoHeight,
        },
    });

    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

async function loadVideo() {
    const video = await setupCamera();
    video.play();

    return video;
}

async function bindPage() {
    let video;

    try {
        video = await loadVideo();
    } catch (e) {
        let info = document.getElementById('info');
        info.textContent = 'this browser does not support video capture,' +
            'or this device does not have a camera';
        info.style.display = 'block';
        throw e;
    }
    const net = await posenet.load();

    console.log(video);
    detectPoseInRealTime(net, video);
}

function detectPoseInRealTime(net, video) {
    const canvas = document.getElementById('output');
    const ctx = canvas.getContext('2d');

    async function poseDetectionFrame() {
        const flipPoseHorizontal = true;

        const imageScaleFactor = 1.0;
        const outputStride = 16;

        const pose = await net.estimateSinglePose(video, imageScaleFactor, flipPoseHorizontal, outputStride);

        canvas.width = videoWidth;
        canvas.height = videoHeight;
        ctx.clearRect(0, 0, videoWidth, videoHeight);
        ctx.save();
        ctx.scale(-1, 1);
        ctx.translate(-videoWidth, 0);
        ctx.drawImage(video, 0, 0, videoWidth, videoHeight);
        if(!x) {
            console.log(pose);
            x = true;
        }
        drawKeypoints(pose['keypoints'], 0.6, ctx);
        ctx.restore();

        requestAnimationFrame(poseDetectionFrame);
    }

    poseDetectionFrame();
}

function domloaded() {
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
// kick off the demo
    bindPage();
}

function getAnalytics(keyPoints) {

}
