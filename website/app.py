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
    <title>CSV Prediction Service</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
        }
        header {
            background: #50b3a2;
            color: #fff;
            padding-top: 30px;
            min-height: 70px;
            border-bottom: #e8491d 3px solid;
        }
        header a {
            color: #fff;
            text-decoration: none;
            text-transform: uppercase;
            font-size: 16px;
        }
        header ul {
            padding: 0;
            list-style: none;
        }
        header li {
            float: left;
            display: inline;
            padding: 0 20px 0 20px;
        }
        header #branding {
            float: left;
        }
        header #branding h1 {
            margin: 0;
        }
        header nav {
            float: right;
            margin-top: 10px;
        }
        .form-container {
            background: #fff;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .form-container h2 {
            margin-top: 0;
        }
        .form-container form {
            margin-bottom: 20px;
        }
        .form-container label {
            display: block;
            margin-bottom: 10px;
        }
        .form-container input[type="file"] {
            margin-bottom: 10px;
        }
        .form-container button {
            background: #50b3a2;
            color: #fff;
            border: 0;
            padding: 10px 20px;
            cursor: pointer;
        }
        .form-container button:hover {
            background: #45a089;
        }
        .download-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div id="branding">
                <h1>CSV Prediction Service</h1>
            </div>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                </ul>
            </nav>
        </div>
    </header>
    <div class="container">
        <div class="form-container">
            <h2>Upload CSV File for Training</h2>
            <form method="POST" action="/upload" enctype="multipart/form-data">
                <label for="file">Upload a CSV file:</label>
                <input type="file" id="file" name="file" accept=".csv" required>
                <button type="submit">Upload</button>
            </form>
        </div>
        <div class="form-container">
            <h2>Upload CSV File for Prediction</h2>
            <form method="POST" action="/predict" enctype="multipart/form-data">
                <label for="file">Upload a CSV file for prediction:</label>
                <input type="file" id="file" name="file" accept=".csv" required>
                <button type="submit">Submit</button>
            </form>
            {% if download_link %}
                <div class="download-link">
                    <h2>Prediction Results:</h2>
                    <a href="{{ download_link }}" download>Download Predictions</a>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE, download_link=None)

@app.route("/upload", methods=["POST"])
def upload():
    # 检查是否有文件上传
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file and file.filename.endswith(".csv"):
        # 保存上传的文件
        input_path = os.path.join("data", file.filename)
        os.makedirs("data", exist_ok=True)  # 确保data目录存在
        file.save(input_path)
        return f"File successfully uploaded to {input_path}", 200

    return "Invalid file format. Please upload a CSV file.", 400

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
        input_path = os.path.join("prompts", file.filename)
        os.makedirs("prompts", exist_ok=True)  # 确保上传目录存在
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