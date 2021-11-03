var socket = null
var username = null
var timer = null
var pc = null
var pc_another = null
$(function (){
    username = document.getElementById("username");
    socket = io('https://' + window.location.host + '/socketio/');
    socket.on('connect', function () {
        if(username){
            username = username.textContent
        }
        else {
            username = null

        }
        socket.emit('self_introduce', {from:username});
    });
    socket.on('connect_error', (error) => {
        // ...
    });
    socket.on('connect_timeout', (timeout) => {
        // ...
    });
    socket.on('reconnect', (attemptNumber) => {
        // ...
    });
    socket.on('reconnect_attempt', (attemptNumber) => {
        // ...
    });
    socket.on('reconnecting', (attemptNumber) => {
        // ...
    });
    socket.on('reconnect_failed', () => {
        // ...
    });
    socket.on('ping', () => {
        // ...
    });
    socket.on('pong', (latency) => {
        // ...
    });
    socket.on('disconnect', () => {

    });
    socket.on('error', (error) => {
        // ...
    });
    socket.on('anonymous_username', (data) => {
        username = data['username'];
        refresh_users()
    });

    socket.on('users_list', (data) => {
        users_list = data['users_list'];
        //获取html元素：在线用户列表，并更新它
        var online_users =document.getElementById("online_users");
        c = online_users.childNodes;
        for (var i=c.length-1; i>=0; i--){
            c[i].remove();
        };
        for(var user of users_list) {
            var li = document.createElement('li');
            li.textContent = user;
            li.onclick= openChoice;
            online_users.appendChild(li);
        }
    });

    socket.on('relay_msg_sig', (data) => {
        user_from = data['from']
        user_to = data['to']
        msg = data['msg']
        sig = data['sig']
        timestamp = data['timestamp']

        var message=document.getElementById("textarea1")
        message.textContent =message.textContent + '\n' + user_from +': '+ user_to +': '+ msg +': '+ sig +' :' + timestamp;

        //接收到信令是SDP Offer
        if(sig === 'sdp_offer')
        {
            //禁止webrtc建立回环连接
            if( user_from !== user_to ) {
                //关闭已经存在的webrtc实例
                if(pc) {
                    pc.close()
                }
                //新建一个webrtc 实例
                pc = new RTCPeerConnection();
                //设置ICE canddiates回调函数
                pc.onicecandidate = function(evt){
                    if(evt.candidate) {
                        //向对端中转该ICE candidates
                        relay_msg_sig(user_from, evt.candidate, "ice");
                    }
                }
                //设置远端媒体轨接收的回调函数
                pc.ontrack = function (evt) {
                    var block_chat = null
                    //获取html元素：远端媒体播放窗
                    var reomte_video = document.getElementById("remote_video")
                    if (reomte_video) {

                    }
                    else {
                        //动态创建html元素：远端媒体播放窗
                        block_chat = document.getElementById("block_chat")
                        reomte_video = document.createElement('video')
                        reomte_video.id = 'remote_video'
                        reomte_video.autoplay = true
                    }
                    //用获取到的track配置远端媒体播放窗的数据源
                    var SRC_OBJECT = 'srcObject' in reomte_video ? reomte_video.srcObject :
                        'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject :
                            'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject : reomte_video.srcObject;
                    var media_stream = null
                    if(SRC_OBJECT === null)
                    {
                        media_stream = new MediaStream;
                        'srcObject' in reomte_video ? reomte_video.srcObject = media_stream :
                            'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject = media_stream :
                                'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject = media_stream : reomte_video.srcObject = media_stream;
                    }
                    else{
                        media_stream = 'srcObject' in reomte_video ? reomte_video.srcObject :
                            'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject :
                                'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject : reomte_video.srcObject;
                    }
                    if(evt.track.kind === "video") {
                        media_stream.addTrack(evt.track)
                    }
                    else if(evt.track.kind === "audio"){
                        media_stream.addTrack(evt.track)
                    }
                    if (block_chat) {
                        block_chat.appendChild(reomte_video)
                    }
                };

                //向webrtc实例设置远端SDP，这里为SDP Offer
                pc.setRemoteDescription(msg);
                //开启本地媒体采集
                getUserMedia({video: true, audio: false},
                    function (stream) {
                        for (const track of stream.getTracks()) {
                            //本地视频轨添加到本地视频播放窗
                            if(track.kind === "video") {
                                var video = document.getElementById('local_video');
                                //将视频流设置为video元素的源
                                var media_stream = new MediaStream;
                                media_stream.addTrack(track)
                                var SRC_OBJECT = 'srcObject' in video ? video.srcObject = media_stream :
                                    'mozSrcObject' in video ? video.mozSrcObject = media_stream :
                                        'webkitSrcObject' in video ? video.webkitSrcObject = media_stream : video.srcObject = media_stream;
                                //播放视频
                                video.play();

                                //本地视频轨添加到webrtc实例中
                                pc.addTrack(track, stream);
                            }
                            else if (track.kind === "audio") {
                                //本地音频轨添加到webrtc实例中
                                pc.addTrack(track, stream);
                            }
                        };

                        //创建webrtc实例的SDP Answer
                        pc.createAnswer().then((desc) => {
                            //设置SDP Answer到本地webrtc实例
                            pc.setLocalDescription(desc)
                            //本地SDP Answer发送到对端
                            relay_msg_sig(user_from, desc, "sdp_answer");
                        });
                    },
                    function () {}
                );
            }
        }
        else if(sig === 'sdp_answer')
        {
            //接到的远端中转信令是SDP Answer，则设置到本地webrtc实例中
            pc.setRemoteDescription(msg).catch((error) => {
                console.error(error);
            });
        }
        else if(sig === 'ice')
        {
            //接到的远端中转信令是ICE candidates，则设置到本地webrtc实例中
            if(user_from === user_to) {

            }
            else {
                pc.addIceCandidate(msg).catch((error) => {
                    console.error(error);
                });
            }
        }
    });

    //配置定时器，定时更新在线用户列表
    timer = setInterval(refresh_users, 2000)

    window.onclose = function () {

    }
});

//获取本地媒体采集实例
function getUserMedia(constrains,success,error){
    if(navigator.mediaDevices.getUserMedia){
        //最新标准API
        navigator.mediaDevices.getUserMedia(constrains).then(success).catch(error);
    } else if (navigator.webkitGetUserMedia){
        //webkit内核浏览器
        navigator.webkitGetUserMedia(constrains).then(success).catch(error);
    } else if (navigator.mozGetUserMedia){
        //Firefox浏览器
        navagator.mozGetUserMedia(constrains).then(success).catch(error);
    } else if (navigator.getUserMedia){
        //旧版API
        navigator.getUserMedia(constrains).then(success).catch(error);
    }
}

//更新在线用户
function refresh_users()
{
    var message = {from: username}
    send_json("list_users", message)
}

//向socket.io发送中转消息的封装函数
function relay_msg_sig(to, msg, sig)
{
    var time=new Date()
    var message = {from:username, to: to, msg: msg, sig: sig, timestamp: time}
    send_json('relay_msg_sig', message)
}

function close_src(){
    if(socket.connected)
    {
        socket.close()
        socket = null
    }

    if(timer) {
        window.clearInterval(timer)
        timer = null
    }

    if(pc)
    {
        pc.close()
        pc = null
    }
}

function send(){
    var message_input = $("input[name='message']");
    var message = message_input.val();
    var message_to =document.getElementById("message_to").textContent;
    if(message_to === '')
    {
        message_to = username;
    }
    //send_json("data", message)
    relay_msg_sig(message_to, message, 'sig')
}

//主动发起webrtc连接的封装函数
function start_chat_online(){
    //关闭已经存在的webrtc实例
    if(pc)
    {
        pc.close()
    }
    //设置消息中转的目的端昵称
    var message_to = document.getElementById("message_to").textContent;
    //如果没有目的端，默认发给自己，用于测试消息中转服务是否正常
    if(message_to === "")
    {
        message_to = username
    }

    //新建webrtc实例
    pc = new RTCPeerConnection();

    //以下与上文类似，差别为这里不是生成SDP Answer，而是生成SDP Offer
    pc.ontrack = function (evt) {
        var block_chat = null
        var reomte_video = document.getElementById("remote_video")
        if (reomte_video) {

        }
        else {
            block_chat = document.getElementById("block_chat")
            reomte_video = document.createElement('video')
            reomte_video.id = 'remote_video'
            reomte_video.autoplay = true
        }
        var SRC_OBJECT = 'srcObject' in reomte_video ? reomte_video.srcObject :
            'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject :
                'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject : reomte_video.srcObject;
        var media_stream = null
        if(SRC_OBJECT === null)
        {
            media_stream = new MediaStream;
            'srcObject' in reomte_video ? reomte_video.srcObject = media_stream :
                'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject = media_stream :
                    'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject = media_stream : reomte_video.srcObject = media_stream;
        }
        else{
            media_stream = 'srcObject' in reomte_video ? reomte_video.srcObject :
                'mozSrcObject' in reomte_video ? reomte_video.mozSrcObject :
                    'webkitSrcObject' in reomte_video ? reomte_video.webkitSrcObject : reomte_video.srcObject;
        }
        if(evt.track.kind === "video") {
            media_stream.addTrack(evt.track)
        }
        else if(evt.track.kind === "audio"){
            media_stream.addTrack(evt.track)
        }

        if (block_chat) {
            block_chat.appendChild(reomte_video)
        }

    };

    pc.onicecandidate = function(evt){
        if(evt.candidate) {
            relay_msg_sig(message_to, evt.candidate, "ice");
        }
    }

    getUserMedia({video: true, audio: true},
        function (stream){
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
                }
                else if (track.kind === "audio") {
                    pc.addTrack(track, stream);
                }
            }
            pc.createOffer().then((desc) =>{
                pc.setLocalDescription(desc)
                relay_msg_sig(message_to, desc, "sdp_offer");
            }).catch((error) => {
                console.error(error);
            });
        },
        function (e) {});

}

function send_json(event, message){
    if(socket.connected)
    {
        socket.emit(event,message);
    }
}