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
        print(f"客户端连接: {websocket.remote_address}")

        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"客户端断开: {websocket.remote_address}")

    async def handle_message(self, websocket, message: str):
        """处理收到的消息."""
        try:
            data = json.loads(message)
            msg_type = data.get("type")

            if msg_type == "action":
                # 用户点击按钮
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

                # 保存到文件
                self.save_feedback(feedback)

                # 发送确认给客户端
                await websocket.send(json.dumps({
                    "type": "ack",
                    "message": f"收到操作: {action}"
                }))

                print(f"[{timestamp}] Slide {slide_index}: {action}")

            elif msg_type == "feedback":
                # 用户提交反馈文本
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

                # 保存到文件
                self.save_feedback(feedback)

                # 发送确认给客户端
                await websocket.send(json.dumps({
                    "type": "ack",
                    "message": f"收到反馈: {feedback_text[:50]}..."
                }))

                print(f"[{timestamp}] Slide {slide_index} feedback: {feedback_text}")

        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "无效的JSON格式"
            }))

    def save_feedback(self, feedback: dict):
        """保存反馈到文件."""
        feedback_dir = Path("workspace/feedback")
        feedback_dir.mkdir(parents=True, exist_ok=True)

        feedback_file = feedback_dir / "feedback_log.json"

        # 读取现有日志
        if feedback_file.exists():
            with open(feedback_file, "r", encoding="utf-8") as f:
                log = json.load(f)
        else:
            log = []

        # 添加新反馈
        log.append(feedback)

        # 保存
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
        print(f"WebSocket服务器启动: ws://{self.host}:{self.port}")
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()  # 永久运行


# 全局服务器实例
server = PreviewServer()


async def start_server():
    """启动预览服务器."""
    await server.start()


def run_server_in_background():
    """在后台运行服务器."""
    asyncio.create_task(start_server())
