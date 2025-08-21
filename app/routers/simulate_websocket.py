from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

router = APIRouter()

@router.websocket("/route/ws/simulate")
async def ws_simulate(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        if data.get("type") != "simulate":
            await websocket.send_json({"error": "expected type=simulate"})
            await websocket.close()
            return
        path = data.get("path", [])
        delay_ms = int(data.get("delay_ms", 300))
        for idx, nid in enumerate(path):
            await websocket.send_json({"step": idx, "node": nid, "total": len(path)})
            await asyncio.sleep(delay_ms / 1000.0)
        await websocket.send_json({"done": True})
        await websocket.close()
    except WebSocketDisconnect:
        pass
    except Exception:
        try:
            await websocket.send_json({"error": "server error"})
            await websocket.close()
        except:
            pass
