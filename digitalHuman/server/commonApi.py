# -*- coding: utf-8 -*-
'''
@File    :   commonApi.py
@Author  :   一力辉 
'''

from digitalHuman.utils import WSConnectionManager, logger
from fastapi import APIRouter, WebSocket


router = APIRouter()
wsCommonManager = WSConnectionManager()

PROBING_SIGNAL_WARN = "Only shpport ping-pong signal, please send ping to keep the connection alive"

@router.websocket("/v0/heartbeat")
async def websocket_heartbeat(websocket: WebSocket):
    await wsCommonManager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await wsCommonManager.send_personal_message("pong", websocket)
            else:
                # 暂不处理其它消息格式: 非探活则关闭接口
                await wsCommonManager.send_personal_message(PROBING_SIGNAL_WARN, websocket)
                logger.error(PROBING_SIGNAL_WARN)
                wsCommonManager.disconnect(websocket)
    except Exception as e:
        logger.error(str(e))
        wsCommonManager.disconnect(websocket)


# from .reponse import BaseResponse, Response
# from fastapi.responses import JSONResponse
# class OutItem(BaseResponse):
#     data: int = 1

# @router.get("/v0/heartbeat", response_model=OutItem, summary="Hearbeat From System")
# async def apiInfer():
#     response = Response()
#     response.ok("SUCCESS")
#     return JSONResponse(content=response.validate(OutItem), status_code=200)