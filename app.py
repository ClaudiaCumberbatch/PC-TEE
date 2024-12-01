from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Increment Service</title>
</head>
<body>
    <h1>Increment Service</h1>
    <form method="POST">
        <label for="value">Enter a number:</label>
        <input type="number" id="value" name="value" required>
        <button type="submit">Submit</button>
    </form>
    {% if result is not none %}
        <h2>Result: {{ result }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        try:
            # 获取用户输入的值并计算结果
            value = int(request.form["value"])
            result = value + 1
        except ValueError:
            result = "Invalid input! Please enter a valid number."
    
    # 渲染 HTML 页面
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    # 启动 HTTPS 服务
    app.run(ssl_context=("cert.pem", "key.pem"), host="0.0.0.0", port=443)