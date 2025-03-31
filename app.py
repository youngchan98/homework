import os
from flask import Flask, request, render_template
import olefile
from bs4 import BeautifulSoup

# Flask 앱 생성
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 업로드 폴더 생성

# HWP 파일에서 텍스트 추출하는 함수
def read_hwp(file_path):
    f = olefile.OleFileIO(file_path)
    encoded_text = f.openstream('PrvText').read()
    decoded_text = encoded_text.decode('utf-16le', errors='ignore')
    soup = BeautifulSoup(decoded_text, "html.parser")
    return soup.get_text(separator="\n")


# 메인 페이지 (파일 업로드 및 분석)
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".hwp"):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)  # 파일 저장
            extracted_text = read_hwp(file_path)  # HWP 내용 추출
            
        
            return render_template("result.html", text=extracted_text)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
