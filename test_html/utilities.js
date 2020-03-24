const videoWidth = 600;
const videoHeight = 500;
var x = false;
var arrayLength = 100;
var dataArray = [];

for(var i = 0; i < arrayLength; i++) {
    dataArray[i] = 0;
}

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

        var keyPoints = pose['keypoints'];

        drawKeypoints(keyPoints, 0.6, ctx);

        if(keyPoints[1]['score'] > 0.6 && keyPoints[2]['score'] > 0.6) {
            var y = getHandAngle(pose['keypoints']);

            dataArray = dataArray.concat(y)
            dataArray.splice(0, 1)

            var data_update = {
                y: [dataArray]
            };

            Plotly.update('angle', data_update);
            drawSegment(toTuple(keyPoints[1]['position']), toTuple(keyPoints[2]['position']), 'red', 1, ctx);
        }

        ctx.restore();

        requestAnimationFrame(poseDetectionFrame);
    }

    poseDetectionFrame();
}

function getHandAngle(keyPoints) {
    var leftHand = keyPoints[1]['position'];
    var rightHand = keyPoints[2]['position'];
    return Math.atan2(rightHand['y'] - leftHand['y'], rightHand['x'] - leftHand['x']) * 180 / Math.PI;
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

    detectPoseInRealTime(net, video);
}

function domloaded() {
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;


    Plotly.newPlot('angle', [{
        y: dataArray,
        mode: 'lines',
        line: {color: '#80CAF6'},
        autosize: false,
        width: 500,
        height: 300,
    }]);

    bindPage();
}

