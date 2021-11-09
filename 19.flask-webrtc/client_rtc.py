# -*- coding: utf-8 -*-
# @author: dengxixi
# @date:   2021-11-03
# @file:   Use python-socketio to connect a server
# python-socketio-5.4.1

from aioice import Candidate
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import socketio
import asyncio
import cv2
from aiortc.rtcicetransport import candidate_from_aioice
from av import VideoFrame

# asyncio
sio = socketio.AsyncClient()


@sio.event
def ready(sid=None):
    print('Ready', sid)


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


class RTSPSwapper(VideoStreamTrack):
    kind = "video"

    def __init__(self, rtsp_url=None):
        super().__init__()
        self.capture = cv2.VideoCapture(rtsp_url )
        print('init ok', self.capture.isOpened())

    async def recv(self):
        timestamp, video_timestamp_base = await self.next_timestamp()
        frame = None
        if self.capture.isOpened():
            ret, frame = self.capture.read()
        # print('-' * 20 , frame.shape)
        frame = VideoFrame.from_ndarray(frame, format="bgr24")
        frame.pts = timestamp
        frame.time_base = video_timestamp_base
        return frame


pc = RTCPeerConnection()


async def offer(params):
    print('get remote offer:', params)
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()

    @pc.on("icecandidate")
    async def icecandidate(xx):
        print("Connect state is %s" % pc.connectionState)
        print("icecandidate is %s" % xx)

    await pc.setRemoteDescription(offer)
    # --------------------------------------- Track RTSP
    [pc.addTrack(RTSPSwapper('rtsp://*:*@192.168.1.100:554/h264/ch1/sub/av_stream')) for t in pc.getTransceivers() if t.kind == "video"]

    # --------------------------------------- Track MediaPlayer
    # player = MediaPlayer(r'C:\Users\dengxixi\Downloads\conan-1000.mp4')
    # for t in pc.getTransceivers():
    #     if t.kind == "audio":
    #         pc.addTrack(player.audio)
    #     elif t.kind == "video":
    #         pc.addTrack(player.video)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    text = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    await sio.emit('data', text)


@sio.event
async def data(data):
    print('received Message : %s' % (data))
    if data is None:
        return
    params = data
    if params.get('type') == 'offer':
        await offer(params)
    elif params.get('type') == 'candidate':
        # desc = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        candidate = params["candidate"].get('candidate')
        ice_candidate = candidate_from_aioice(Candidate.from_sdp(candidate))
        ice_candidate.sdpMid = params["candidate"].get('sdpMid')
        ice_candidate.sdpMLineIndex = params["candidate"].get('sdpMLineIndex')
        await pc.addIceCandidate(ice_candidate)
        text = {"candidate": params["candidate"], "type": 'candidate'}
        await sio.emit('data', text)

    elif params.get('type') == 'answer':
        desc = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        await pc.setRemoteDescription(desc)


async def start():
    await sio.connect('http://localhost:5001')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.run_forever()
