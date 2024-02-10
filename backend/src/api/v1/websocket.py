from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


# @router.websocket("")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


@router.websocket("test/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    print("got ws request!")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{client_id}: Message text was: {data}")
    except WebSocketDisconnect:
        print("disconnected")
