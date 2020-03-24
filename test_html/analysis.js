/**
 0: {score: 0.999999999999999, part: "nose", position: {x: , y: }}
 1: {score: 0.999441921710968, part: "leftEye", position: {…}}
 2: {score: 0.9995291233062744, part: "rightEye", position: {…}}
 3: {score: 0.9552914500236511, part: "leftEar", position: {…}}
 4: {score: 0.9137577414512634, part: "rightEar", position: {…}}
 5: {score: 0.7450869679450989, part: "leftShoulder", position: {…}}
 6: {score: 0.8452247381210327, part: "rightShoulder", position: {…}}
 7: {score: 0.061146918684244156, part: "leftElbow", position: {…}}
 8: {score: 0.045826539397239685, part: "rightElbow", position: {…}}
 9: {score: 0.023628393188118935, part: "leftWrist", position: {…}}
 10: {score: 0.020958352833986282, part: "rightWrist", position: {…}}
 11: {score: 0.008425146341323853, part: "leftHip", position: {…}}
 12: {score: 0.016337966546416283, part: "rightHip", position: {…}}
 13: {score: 0.008990046568214893, part: "leftKnee", position: {…}}
 14: {score: 0.01072282437235117, part: "rightKnee", position: {…}}
 15: {score: 0.006702173966914415, part: "leftAnkle", position: {…}}
 16: {score: 0.004427269101142883, part: "rightAnkle
 */

function getCenter(keyPoints) {
    var leftShoulder = keyPoints[5]['position'];
    var rightShoulder = keyPoints[6]['position'];
    return toTuple((leftShoulder['x'] + rightShoulder['x'])/2,
        (leftShoulder['y'] + rightShoulder['y'])/2);
}

function getHandAngle(keyPoints) {
    var lefttHand = keyPoints[5]['position'];
    var rightHand = keyPoints[6]['position'];
    return Math.atan2(rightHand['y'] - lefttHand['y'], rightHand['x'] - lefttHand['x']) * 180 / Math.PI;
}