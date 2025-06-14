from flask import Flask, request, send_file, render_template
import threads_downloader

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    username = request.form.get("username")
    if not username:
        return "กรุณากรอกชื่อผู้ใช้ Threads", 400
    zip_path = threads_downloader.download_from_threads(username)
    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
