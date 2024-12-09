from flask import Flask, request, render_template_string, send_file, jsonify
import pandas as pd
import os
import subprocess

app = Flask(__name__)

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Predict Service</title>
</head>
<body>
    <h1>CSV Prediction Service</h1>
    <form method="POST" action="/predict" enctype="multipart/form-data">
        <label for="file">Upload a CSV file:</label>
        <input type="file" id="file" name="file" accept=".csv" required>
        <button type="submit">Submit</button>
    </form>
    {% if download_link %}
        <h2>Prediction Results:</h2>
        <a href="{{ download_link }}" download>Download Predictions</a>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE, download_link=None)

@app.route("/predict", methods=["POST"])
def predict():
    # 检查是否有文件上传
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file and file.filename.endswith(".csv"):
        # 保存上传的文件
        input_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)  # 确保上传目录存在
        file.save(input_path)

        # 调用 predict.py 进行预测
        try:
            subprocess.check_output(["python", "predict.py", input_path], universal_newlines=True)
        except subprocess.CalledProcessError as e:
            return f"Error running prediction: {e.output}", 500

        # 返回生成的 predictions.csv 文件
        output_path = "predictions.csv"
        return render_template_string(HTML_TEMPLATE, download_link=output_path)

    return "Invalid file format. Please upload a CSV file.", 400

@app.route("/predictions.csv", methods=["GET"])
def download_predictions():
    return send_file("predictions.csv", as_attachment=True)

if __name__ == "__main__":
    # 启动 HTTPS 服务
    app.run(ssl_context=("cert.pem", "key.pem"), host="0.0.0.0", port=443)