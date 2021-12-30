from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
with open('index.html', 'r') as f:
    html = f.read()

@app.get('/')
async def get_index():
    return HTMLResponse(html)

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    message_id = 1
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            data['message_id'] = message_id
            message_id += 1
            data = json.dumps(data)
            await websocket.send_text(f'{data}')
    except WebSocketDisconnect:
        message_id = 1