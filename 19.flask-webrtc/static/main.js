'use strict';

var isChannelReady = false;
var isInitiator = false;
var isStarted = false;
var localStream;
var pc;
var remoteStream;
var turnReady;
var receiveChannel;
var sendChannel;
var sendText = document.querySelector("#text");
var chatlog = document.querySelector('#chatlog');
var nameText = document.querySelector("#username")

var pcConfig = {
    'iceServers': [{
        'urls': 'stun:stun.l.google.com:19302'
    }]
};

// Set up audio and video regardless of what devices are present.
var sdpConstraints = {
    offerToReceiveAudio: true,
    offerToReceiveVideo: true
};

/////////////////////////////////////////////

//room = 'foo';
// Could prompt for room name:
// var room = prompt('Enter room name:');

var socket = io.connect();

if (room !== '') {
    socket.emit('create_or_join', room);
    console.log('Attempted to create or  join room', room);
}

socket.on('message', function (message) {
    console.log('Client received message:', message);
    if (typeof message == "string") {
        var text = document.createElement("P");
        text.appendChild(document.createTextNode(msg));
        chatlog.appendChild(text);
        // maybeStart();
    } else if (message.type === 'offer') {
        if (!isInitiator && !isStarted) {
            maybeStart();
        }
        pc.setRemoteDescription(new RTCSessionDescription(message));
        doAnswer();
    } else if (message.type === 'answer' && isStarted) {
        pc.setRemoteDescription(new RTCSessionDescription(message));
    } else if (message.type === 'candidate' && isStarted) {
        var candidate = new RTCIceCandidate({
            sdpMLineIndex: message.label,
            candidate: message.candidate
        });
        pc.addIceCandidate(candidate);
    } else if (message === 'bye' && isStarted) {
        handleRemoteHangup();
    }
    console.log('------------------------------------')

})

socket.on('join', function (room) {
    console.log('join success', room)
    isChannelReady = true;
    isInitiator = true;
});


socket.on('log', function (array) {
    console.log('----------socket log')
    console.log.apply(console, array);
});

////////////////////////////////////////////////

function sendMessage(message) {
    console.log('Client sending message: ', message);
    socket.emit('message', message);
}

var localVideo = document.querySelector('#localVideo');
var remoteVideo = document.querySelector('#remoteVideo');

navigator.mediaDevices.getUserMedia({
    audio: false,
    video: true
}).then(gotStream).catch(function (e) {
    // alert('getUserMedia() error: ' + e.name);
    console.log('XXXXXXXXXXXXXXXXX: getUserMedia() error: ' + e.name)
    createPeerConnection()
    doCall()
});

function gotStream(stream) {
    console.log('Adding local stream.');
    localVideo.src = window.URL.createObjectURL(stream);
    localStream = stream;
    // sendMessage('got user media');
    if (isInitiator) {
        maybeStart();
    }
}

var constraints = {
    video: true
};

console.log('Getting user media with constraints', constraints);

// if (false) {
//     requestTurn(
//         'https://computeengineondemand.appspot.com/turn?username=41784574&key=4080218913'
//     );
// }

function maybeStart() {
    console.log('>>>>>>> maybeStart() ')
    console.log("isStarted:", isStarted, "localStream:", localStream, "isChannelReady:", isChannelReady);

    if (!isStarted && typeof localStream !== 'undefined' && isChannelReady) {
        console.log('>>>>>> creating peer connection');
        createPeerConnection();
        pc.addStream(localStream);
        isStarted = true;
        console.log('isInitiator', isInitiator);
        if (isInitiator) {
            doCall();
        }
    } else {

    }
}

window.onbeforeunload = function () {
    socket.emit('disconnect', room)
    console.log("sending disconnect")
};

// 主动发起webrtc连接的封装函数
function start_chat_online() {
    //关闭已经存在的webrtc实例
    if (pc) {
        pc.close()
    }
    //设置消息中转的目的端昵称
    var message_to = document.getElementById("message_to").textContent;
    //如果没有目的端，默认发给自己，用于测试消息中转服务是否正常
    if (message_to === "") {
        message_to = username
    }

    //新建webrtc实例
    pc = new RTCPeerConnection();

    //以下与上文类似，差别为这里不是生成SDP Answer，而是生成SDP Offer
    pc.ontrack = function (evt) {
        var block_chat = null
        var reomte_video = document.getElementById("remote_video")
        if (reomte_video) {

        } else {
            block_chat = document.getElementById("block_chat")
            reomte_video = document.createElement('video')
            reomte_video.id = 'remote_video'
            reomte_video.autoplay = true
        }
        var SRC_OBJECT = 'srcObject' in reomte_video ? reomte_video.srcObject :
            'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject :
                'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject : reomte_video.srcObject;
        var media_stream = null
        if (SRC_OBJECT === null) {
            media_stream = new MediaStream;
            'srcObject' in reomte_video ? reomte_video.srcObject = media_stream :
                'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject = media_stream :
                    'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject = media_stream : reomte_video.srcObject = media_stream;
        } else {
            media_stream = 'srcObject' in reomte_video ? reomte_video.srcObject :
                'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject :
                    'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject : reomte_video.srcObject;
        }
        if (evt.track.kind === "video") {
            media_stream.addTrack(evt.track)
        } else if (evt.track.kind === "audio") {
            media_stream.addTrack(evt.track)
        }

        if (block_chat) {
            block_chat.appendChild(reomte_video)
        }

    };

    pc.onicecandidate = function (evt) {
        if (evt.candidate) {
            relay_msg_sig(message_to, evt.candidate, "ice");
        }
    }

    getUserMedia({video: true, audio: true},
        function (stream) {
            for (const track of stream.getTracks()) {
                if (track.kind === "video") {
                    var video = document.getElementById('local_video');
                    var media_stream = new MediaStream;
                    media_stream.addTrack(track)
                    //将视频流设置为video元素的源
                    var SRC_OBJECT = 'srcObject' in video ? video.srcObject = media_stream :
                        'mozSrcObject' in video ? video.mozSrcObject = media_stream :
                            'webkitSrcObject' in video ? video.webkitSrcObject = media_stream : video.srcObject = media_stream;

                    //播放视频
                    video.play();

                    pc.addTrack(track, stream);
                } else if (track.kind === "audio") {
                    pc.addTrack(track, stream);
                }
            }
            pc.createOffer().then((desc) => {
                pc.setLocalDescription(desc)
                relay_msg_sig(message_to, desc, "sdp_offer");
            }).catch((error) => {
                console.error(error);
            });
        },
        function (e) {
        });

}


/////////////////////////////////////////////////////////

function createPeerConnection() {
    try {
        pc = new RTCPeerConnection(pcConfig);
        sendChannel = pc.createDataChannel('chat', null);
        console.log('sendChannel', sendChannel)

        pc.onicecandidate = handleIceCandidate;
        pc.onaddstream = handleRemoteStreamAdded;
        pc.onremovestream = handleRemoteStreamRemoved;
        pc.ondatachannel = handleChannelCallback;

        console.log('Created RTCPeerConnnection');
    } catch (e) {
        console.log('Failed to create PeerConnection, exception: ' + e.message);
        alert('Cannot create RTCPeerConnection object.');
        return;
    }
}

function handleChannelCallback(event) {
    receiveChannel = event.channel;
    receiveChannel.onmessage = onReceiveMessageCallback;
}

function onReceiveMessageCallback(event) {
    var text = document.createElement("P");
    text.appendChild(document.createTextNode(event.data))

    chatlog.appendChild(text);
}

function handleIceCandidate(event) {
    console.log('icecandidate event: ', event);
    if (event.candidate) {
        sendMessage({
            type: 'candidate',
            label: event.candidate.sdpMLineIndex,
            id: event.candidate.sdpMid,
            candidate: event.candidate.candidate
        });
    } else {
        console.log('End of candidates.');
    }
}

function sendData() {
    if (sendChannel) {
        console.log('sendChannel.readyState:', sendChannel.readyState)
        if (sendChannel.readyState === 'open') {
            sendChannel.send(nameText.value + ':' + sendText.value);
            sendText.value = '';
        }

    } else {
        sendMessage(nameText.value + ':' + sendText.value)
    }

    // var text = document.createElement("P");
    // text.appendChild(document.createTextNode(sendText.value));
    // chatlog.appendChild(text);

}

function handleRemoteStreamAdded(event) {
    console.log('Remote stream added.');
    remoteVideo.src = window.URL.createObjectURL(event.stream);
    remoteStream = event.stream;
}

function handleCreateOfferError(event) {
    console.log('createOffer() error: ', event);
}

function doCall() {
    console.log('Sending offer to peer');
    pc.createOffer(setLocalAndSendMessage, handleCreateOfferError);
}

function doAnswer() {
    console.log('Sending answer to peer.');
    pc.createAnswer().then(
        setLocalAndSendMessage,
        onCreateSessionDescriptionError
    );
}

function setLocalAndSendMessage(sessionDescription) {
    // Set Opus as the preferred codec in SDP if Opus is present.
    //  sessionDescription.sdp = preferOpus(sessionDescription.sdp);
    pc.setLocalDescription(sessionDescription);
    console.log('setLocalAndSendMessage sending message', sessionDescription);
    sendMessage(sessionDescription);
}

function onCreateSessionDescriptionError(error) {
    //trace('Failed to create session description: ' + error.toString());
}

function requestTurn(turnURL) {
    var turnExists = false;
    for (var i in pcConfig.iceServers) {
        if (pcConfig.iceServers[i].urls.substr(0, 5) === 'turn:') {
            turnExists = true;
            turnReady = true;
            break;
        }
    }
    if (!turnExists) {
        console.log('Getting TURN server from ', turnURL);
        // No TURN server. Get one from computeengineondemand.appspot.com:
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var turnServer = JSON.parse(xhr.responseText);
                console.log('Got TURN server: ', turnServer);
                pcConfig.iceServers.push({
                    'url': 'turn:' + turnServer.username + '@' + turnServer.turn,
                    'credential': turnServer.password
                });
                turnReady = true;
            }
        };
        xhr.open('GET', turnURL, true);
        xhr.send();
    }
}

function handleRemoteStreamRemoved(event) {
    console.log('Remote stream removed. Event: ', event);
}

function hangup() {
    console.log('Hanging up.');
    stop();
    sendMessage('bye');
}

function handleRemoteHangup() {
    console.log('Session terminated.');
    stop();
    isInitiator = false;
}

function stop() {
    isStarted = false;
    // isAudioMuted = false;
    // isVideoMuted = false;
    pc.close();
    pc = null;
}

///////////////////////////////////////////

// Set Opus as the default audio codec if it's present.
function preferOpus(sdp) {
    var sdpLines = sdp.split('\r\n');
    var mLineIndex;
    // Search for m line.
    for (var i = 0; i < sdpLines.length; i++) {
        if (sdpLines[i].search('m=audio') !== -1) {
            mLineIndex = i;
            break;
        }
    }
    if (mLineIndex === null) {
        return sdp;
    }

    // If Opus is available, set it as the default in m line.
    for (i = 0; i < sdpLines.length; i++) {
        if (sdpLines[i].search('opus/48000') !== -1) {
            var opusPayload = extractSdp(sdpLines[i], /:(\d+) opus\/48000/i);
            if (opusPayload) {
                sdpLines[mLineIndex] = setDefaultCodec(sdpLines[mLineIndex],
                    opusPayload);
            }
            break;
        }
    }

    // Remove CN in m line and sdp.
    sdpLines = removeCN(sdpLines, mLineIndex);

    sdp = sdpLines.join('\r\n');
    return sdp;
}

function extractSdp(sdpLine, pattern) {
    var result = sdpLine.match(pattern);
    return result && result.length === 2 ? result[1] : null;
}

// Set the selected codec to the first in m line.
function setDefaultCodec(mLine, payload) {
    var elements = mLine.split(' ');
    var newLine = [];
    var index = 0;
    for (var i = 0; i < elements.length; i++) {
        if (index === 3) { // Format of media starts from the fourth.
            newLine[index++] = payload; // Put target payload to the first.
        }
        if (elements[i] !== payload) {
            newLine[index++] = elements[i];
        }
    }
    return newLine.join(' ');
}

// Strip CN from sdp before CN constraints is ready.
function removeCN(sdpLines, mLineIndex) {
    var mLineElements = sdpLines[mLineIndex].split(' ');
    // Scan from end for the convenience of removing an item.
    for (var i = sdpLines.length - 1; i >= 0; i--) {
        var payload = extractSdp(sdpLines[i], /a=rtpmap:(\d+) CN\/\d+/i);
        if (payload) {
            var cnPos = mLineElements.indexOf(payload);
            if (cnPos !== -1) {
                // Remove CN payload from m line.
                mLineElements.splice(cnPos, 1);
            }
            // Remove CN line in sdp
            sdpLines.splice(i, 1);
        }
    }

    sdpLines[mLineIndex] = mLineElements.join(' ');
    return sdpLines;
}