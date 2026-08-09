from fastapi import WebSocket, APIRouter, WebSocketDisconnect

router = APIRouter(prefix="/ws")

@router.websocket("/")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Disconnected")