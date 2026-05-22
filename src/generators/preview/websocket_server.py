"""WebSocket服务器 - 实现HTML预览与Claude Code的实时通信."""

import asyncio
import websockets
import json
from pathlib import Path
from datetime import datetime


class PreviewServer:
    """预览服务器，处理HTML页面与Claude Code的通信."""

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.feedback_history = []

    async def handler(self, websocket):
        """处理WebSocket连接."""
        self.clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")

        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected: {websocket.remote_address}")

    async def handle_message(self, websocket, message: str):
        """处理收到的消息."""
        try:
            data = json.loads(message)
            msg_type = data.get("type")

            if msg_type == "action":
                action = data.get("action")
                slide_index = data.get("slide")
                timestamp = data.get("timestamp")

                feedback = {
                    "type": "action",
                    "action": action,
                    "slide": slide_index,
                    "timestamp": timestamp
                }
                self.feedback_history.append(feedback)
                self.save_feedback(feedback)

                await websocket.send(json.dumps({
                    "type": "ack",
                    "message": f"Received action: {action}"
                }))

                print(f"[{timestamp}] Slide {slide_index}: {action}")

            elif msg_type == "feedback":
                feedback_text = data.get("feedback")
                slide_index = data.get("slide")
                timestamp = data.get("timestamp")

                feedback = {
                    "type": "text_feedback",
                    "feedback": feedback_text,
                    "slide": slide_index,
                    "timestamp": timestamp
                }
                self.feedback_history.append(feedback)
                self.save_feedback(feedback)

                await websocket.send(json.dumps({
                    "type": "ack",
                    "message": f"Feedback received"
                }))

                print(f"[{timestamp}] Slide {slide_index} feedback: {feedback_text}")

        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Invalid JSON"
            }))

    def save_feedback(self, feedback: dict):
        """保存反馈到文件."""
        feedback_dir = Path("workspace/feedback")
        feedback_dir.mkdir(parents=True, exist_ok=True)
        feedback_file = feedback_dir / "feedback_log.json"

        if feedback_file.exists():
            with open(feedback_file, "r", encoding="utf-8") as f:
                log = json.load(f)
        else:
            log = []

        log.append(feedback)

        with open(feedback_file, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)

    async def broadcast(self, message: str):
        """向所有客户端广播消息."""
        if self.clients:
            await asyncio.gather(
                *[client.send(message) for client in self.clients]
            )

    async def start(self):
        """启动服务器."""
        print(f"WebSocket server started: ws://{self.host}:{self.port}")
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()


server = PreviewServer()


async def start_server():
    await server.start()