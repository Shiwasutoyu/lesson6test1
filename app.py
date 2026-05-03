# 標準ライブラリのみで動作するBMI計算Webアプリ
# Render / ローカル両対応
# python app.py で起動

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

PORT = int(os.environ.get("PORT", 8000))

def calc_bmi(height_cm, weight_kg):
    """BMI計算と評価"""
    try:
        h = float(height_cm) / 100
        w = float(weight_kg)
        if h <= 0:
            return 0, "不明"
        bmi = w / (h * h)
    except:
        return 0, "不明"

    if bmi < 18.5:
        result = "低体重"
    elif bmi < 25:
        result = "標準"
    elif bmi < 30:
        result = "肥満(軽度)"
    elif bmi < 35:
        result = "肥満(中等度)"
    elif bmi < 40:
        result = "肥満(高度)"
    else:
        result = "肥満(重度)"

    return round(bmi, 2), result


class Handler(BaseHTTPRequestHandler):

    def render(self, bmi="", result="", height="", weight=""):
        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>BMI計算機</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background:#f4f6f8;
    padding:40px;
}}

.container {{
    max-width:420px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:10px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
}}

h1 {{
    text-align:center;
}}

input {{
    width:100%;
    padding:10px;
    margin-top:8px;
    margin-bottom:16px;
    font-size:16px;
}}

button {{
    padding:10px 15px;
    font-size:16px;
    margin-right:10px;
}}

.result {{
    margin-top:20px;
    padding:10px;
    background:#eef6ff;
    border-radius:6px;
}}
</style>

<script>
function clearForm(){{
    document.getElementById("height").value="";
    document.getElementById("weight").value="";
}}
</script>

</head>

<body>

<div class="container">
<h1>BMI計算機</h1>

<form method="POST">
<label>身長(cm)</label>
<input id="height" name="height" value="{height}" placeholder="例:170">

<label>体重(kg)</label>
<input id="weight" name="weight" value="{weight}" placeholder="例:65">

<button type="submit">計算</button>
<button type="button" onclick="clearForm()">入力をリセット</button>
</form>

<div class="result">
BMI : {bmi}<br>
判定 : {result}
</div>

</div>

</body>
</html>
"""
        return html

    def do_GET(self):
        html = self.render()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)

        height = data.get("height", ["0"])[0]
        weight = data.get("weight", ["0"])[0]

        bmi, result = calc_bmi(height, weight)

        html = self.render(bmi, result, height, weight)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Server running on port {PORT}")
    server.serve_forever()