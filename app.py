from flask import Flask, render_template

app = Flask(__name__)

# 곤충 데이터 (ID별 고유 정보 - 나중에 JSON이나 DB로 확장 가능)
insects = {
    "1": {"name": "사슴벌레", "description": "사슴벌레는 큰 뿔이 특징인 곤충으로, 숲속에서 주로 발견됩니다. 여름철에 활발합니다.", "image": "stag_beetle.jpg"},
    "2": {"name": "나비", "description": "나비는 화려한 날개를 가진 곤충으로, 꽃가루를 옮기는 역할을 합니다. 봄~가을에 볼 수 있습니다.", "image": "butterfly.jpg"},
    "3": {"name": "매미", "description": "매미는 여름에 큰 소리로 우는 고충으로, 나무에서 삽니다. 수컷이 울음소리를 냅니다.", "image": "cicada.jpg"},
    # 더 추가하려면: "4": {"name": "새 곤충", "description": "...", "image": "new.jpg"},
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/insect/<id>")
def insect_info(id):
    insect = insects.get(id, {"name": "알 수 없음", "description": "정보가 없습니다.", "image": ""})
    return render_template("insect.html", insect=insect)

if __name__ == "__main__":
    app.run(debug=True)