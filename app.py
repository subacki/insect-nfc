from flask import Flask, render_template

app = Flask(__name__)

# 곤충 데이터 (이름을 키로 사용 - URL: /insect/<이름>)
insects = {
    "bee": {"name": "벌", "description": "벌은 꿀을 만드는 곤충입니다. 꽃을 방문해 꽃가루를 옮겨주고, 벌집에서 함께 삽니다. 조심하세요, 쏘면 아프답니다!", "image": "bee.jpg"},
    "larva": {"name": "애벌래", "description": "유충은 곤충의 새끼 단계예요. 나비나 벌의 유충이 있으며, 먹이를 많이 먹으며 성장합니다. 나중에 예쁜 곤충이 돼요!", "image": "larva.jpg"},
    "mosquito": {"name": "모기", "description": "모기는 피를 빨아먹는 곤충으로, 여름에 많이 나타납니다. 모기장으로 피하세요. 밤에 조심해야 해요!", "image": "mosquito.jpg"},
    "ladybug": {"name": "무당벌레", "description": "무당벌레는 빨간 점이 있는 귀여운 곤충입니다. 해충을 잡아먹어 농사를 도와줘요. 행운의 상징이에요!", "image": "ladybug.jpg"},
    "butterfly": {"name": "나비", "description": "나비는 아름다운 날개를 가진 곤충입니다. 꽃가루를 옮기는 역할을 하며, 봄과 여름에 꽃밭에서 춤을 춥니다.", "image": "butterfly.jpg"},
}

@app.route("/")
def home():
    return render_template("index.html", insects=insects)

@app.route("/insect/<insect_name>")
def insect_info(insect_name):
    insect = insects.get(insect_name, {"name": "알 수 없음 😕", "description": "이 곤충은 아직 정보가 없어요. 더 찾아보세요!", "image": ""})
    return render_template("insect.html", insect=insect)

if __name__ == "__main__":
    app.run(debug=True)