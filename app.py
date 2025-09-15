from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# --- 설정 ---
app.config['SECRET_KEY'] = 'a_very_secret_and_complex_key_for_session'
# ⚠️ 최종 확인했던 본인의 DB 정보로 설정해주세요.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:qnsker@localhost:3307/bug_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 확장 기능 초기화 ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "로그인이 필요한 기능입니다."

# --- 데이터베이스 모델 ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    progress = db.relationship('LearningProgress', backref='user', uselist=False, cascade="all, delete-orphan")

class LearningProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completed_lessons = db.Column(db.Text, default='')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- 곤충 데이터 ---
insects = {
    "bee": {"name": "꿀벌", "description": "윙윙~ 나는야 꿀벌! 꽃을 찾아다니며 달콤한 꿀을 모으는 작은 요리사란다. 꽃들에게 꽃가루를 옮겨주며 열매를 맺게 도와주는 아주 중요한 친구이기도 해. 하지만 깜짝 놀라게 하면 침으로 콕! 쏠 수 있으니 조심해야 해!", "image": "bee.jpg"},
    "larva": {"name": "애벌레", "description": "꿈틀꿈틀, 나는 애벌레야! 지금은 작고 통통하지만, 나뭇잎을 아주 많이 먹고 나면 곧 멋진 나비나 나방으로 변신할 준비를 한단다. 나의 변신 과정을 지켜봐 줄래? 정말 신기할 거야!", "image": "larva.jpg"},
    "mosquito": {"name": "모기", "description": "에엥~ 여름밤의 작은 손님, 모기야. 암컷 모기들은 아기 모기를 위해 영양분이 가득한 피를 찾아다녀. 그래서 사람이나 동물을 살짝 물기도 하지. 하지만 수컷 모기들은 꽃의 꿀을 먹고 사는 채식주의자란다!", "image": "mosquito.jpg"},
    "ladybug": {"name": "무당벌레", "description": "안녕! 나는 행운을 가져다주는 무당벌레야. 빨갛고 동그란 등에 까만 점이 콕콕 박혀있지. 농작물을 아프게 하는 진딧물을 냠냠 잡아먹어서 농부 아저씨들이 아주 좋아하는 고마운 곤충이란다.", "image": "ladybug.jpg"},
    "butterfly": {"name": "나비", "description": "하늘하늘, 나는 꽃의 친구 나비야! 활짝 편 날개에는 아름다운 그림이 그려져 있어. 애벌레 시절을 거쳐 번데기 안에서 참고 기다리면, 이렇게 멋진 날개를 가진 어른 나비로 다시 태어난단다. 꽃밭에서 춤추는 나를 찾아봐!", "image": "butterfly.jpg"},
}

# --- 라우팅 ---
@app.route("/")
def home():
    stats = {}
    # 로그인 상태를 boolean 값으로 템플릿에 전달
    is_authenticated = current_user.is_authenticated
    
    if is_authenticated:
        completed_set = set(filter(None, current_user.progress.completed_lessons.split(',')))
        stats['total_insects'] = len(insects)
        stats['completed_count'] = len(completed_set)
        stats['progress_percentage'] = int((len(completed_set) / len(insects)) * 100) if insects else 0
        
    return render_template("index.html", stats=stats, is_authenticated=is_authenticated)

# ... 나머지 insect_info, login, register, logout 라우트는 이전과 동일합니다 ...
@app.route("/insect/<insect_name>")
def insect_info(insect_name):
    if insect_name not in insects:
        return "해당 곤충을 찾을 수 없습니다.", 404
    if current_user.is_authenticated:
        progress = current_user.progress
        completed_set = set(filter(None, progress.completed_lessons.split(',')))
        if insect_name not in completed_set:
            completed_set.add(insect_name)
            progress.completed_lessons = ','.join(sorted(list(completed_set)))
            db.session.commit()
    return render_template("insect.html", insect=insects[insect_name])

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form['password']):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            flash('아이디 또는 비밀번호가 올바르지 않습니다.')
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('이미 사용 중인 아이디입니다.')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=request.form['username'], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        new_progress = LearningProgress(user_id=new_user.id)
        db.session.add(new_progress)
        db.session.commit()

        flash('회원가입이 완료되었습니다! 로그인해주세요.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)