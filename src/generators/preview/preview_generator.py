"""预览生成器 - 生成HTML/图片/PPT预览."""

from pathlib import Path
import json


class PreviewGenerator:
    """预览生成器，支持多种预览格式."""

    def __init__(self, output_dir: str = "workspace/preview"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html_preview(self, slide_data: dict, slide_index: int) -> str:
        """生成HTML预览文件（含WebSocket客户端）."""
        html_content = self._create_html_template(slide_data, slide_index)
        html_path = self.output_dir / f"slide_{slide_index}.html"

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(html_path)

    def _create_html_template(self, slide_data: dict, slide_index: int) -> str:
        """创建HTML模板（含WebSocket客户端）."""
        title = slide_data.get("title", f"Slide {slide_index}")
        content = slide_data.get("content", "")
        notes = slide_data.get("notes", "")
        duration = slide_data.get("duration_seconds", 60)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: #003366; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .slide {{ background: white; border: 1px solid #ddd; padding: 40px; min-height: 400px; }}
        .controls {{ background: white; border: 1px solid #ddd; border-top: none; padding: 20px; }}
        .btn {{ padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; margin-right: 10px; }}
        .btn-confirm {{ background: #27ae60; color: white; }}
        .btn-modify {{ background: #f39c12; color: white; }}
        .btn-skip {{ background: #95a5a6; color: white; }}
        .btn-redo {{ background: #e74c3c; color: white; }}
        .feedback {{ background: white; border: 1px solid #ddd; border-top: none; padding: 20px; border-radius: 0 0 8px 8px; }}
        .feedback textarea {{ width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; min-height: 80px; }}
        .status {{ margin-top: 15px; padding: 10px; border-radius: 4px; display: none; }}
        .status.show {{ display: block; background: #d4edda; color: #155724; }}
        .connection {{ font-size: 12px; margin-top: 10px; }}
        .connected {{ color: #27ae60; }}
        .disconnected {{ color: #e74c3c; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Slide {slide_index}</h1>
            <div class="meta">Duration: {duration}s</div>
            <div id="connStatus" class="connection disconnected">Not connected</div>
        </div>
        <div class="slide">
            <h2>{title}</h2>
            <p>{content}</p>
        </div>
        <div class="controls">
            <button class="btn btn-confirm" onclick="send('confirm')">Confirm</button>
            <button class="btn btn-modify" onclick="send('modify')">Modify</button>
            <button class="btn btn-skip" onclick="send('skip')">Skip</button>
            <button class="btn btn-redo" onclick="send('redo')">Redo</button>
        </div>
        <div class="feedback">
            <h3>Feedback</h3>
            <textarea id="feedbackInput" placeholder="Enter feedback..."></textarea>
            <button class="btn btn-modify" onclick="submitFeedback()">Submit</button>
        </div>
        <div id="status" class="status"></div>
    </div>
    <script>
        let ws = null;
        const SLIDE = {slide_index};

        function connect() {{
            ws = new WebSocket('ws://localhost:8765');
            ws.onopen = () => {{
                document.getElementById('connStatus').textContent = 'Connected';
                document.getElementById('connStatus').className = 'connection connected';
            }};
            ws.onmessage = (e) => {{
                const d = JSON.parse(e.data);
                showStatus(d.message);
            }};
            ws.onclose = () => {{
                document.getElementById('connStatus').textContent = 'Disconnected';
                document.getElementById('connStatus').className = 'connection disconnected';
                setTimeout(connect, 3000);
            }};
        }}

        function send(action) {{
            if (ws && ws.readyState === 1) {{
                ws.send(JSON.stringify({{ type: 'action', action, slide: SLIDE, timestamp: new Date().toISOString() }}));
            }}
        }}

        function submitFeedback() {{
            const fb = document.getElementById('feedbackInput').value;
            if (fb && ws && ws.readyState === 1) {{
                ws.send(JSON.stringify({{ type: 'feedback', feedback: fb, slide: SLIDE, timestamp: new Date().toISOString() }}));
                document.getElementById('feedbackInput').value = '';
            }}
        }}

        function showStatus(msg) {{
            const s = document.getElementById('status');
            s.textContent = msg;
            s.className = 'status show';
            setTimeout(() => s.className = 'status', 3000);
        }}

        window.onload = connect;
    </script>
</body>
</html>"""
        return html