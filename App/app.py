from flask import Flask, render_template, redirect, url_for, request, flash
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from datetime import datetime
from scheduler_alg import ScheduleManager  # Import the ScheduleManager class
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Scheduler"
app.secret_key = 'your_secret_key'
mongo = PyMongo(app)
db = mongo.db
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource="admin")
    db = client["scheduler_db"]
    return db

class User(UserMixin):
    def __init__(self, user_json):
        self.id = user_json.get('_id')
        self.username = user_json.get('username')
        self.password_hash = user_json.get('password')
        self.status = user_json.get('status')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None
    return User(user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.users.find_one({'username': username})
        if user and User(user).check_password(password):
            user_obj = User(user)
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == (['POST']):
        username = request.form.get('username')
        password = request.form.get('password')
        if db.users.find_one({'username': username}):
            flash('Username already exists.')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.users.insert_one({'username': username, 'password': hashed_password, 'status': "student"})
            flash('User created successfully.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user_role = current_user.status if hasattr(current_user, 'status') else 'student'
    return render_template('admin_only.html', user=current_user, role=user_role)

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'POST':
        day = request.form.get('day')
        in_time_str = request.form.get('inTime')
        out_time_str = request.form.get('outTime')

        in_time = datetime.strptime(in_time_str, '%H:%M').time()
        out_time = datetime.strptime(out_time_str, '%H:%M').time()

        in_time_str = in_time.strftime('%H:%M')
        out_time_str = out_time.strftime('%H:%M')

        db.schedule.insert_one({'user_id': current_user.id, 'day': day, 'in_time': in_time_str, 'out_time': out_time_str})
        
        flash('Schedule submitted successfully.')
        return redirect(url_for('dashboard'))
    return render_template('student_submit_schedule.html')

@app.route('/view_schedule', methods=['GET'])
@login_required
def view_schedule():
    schedule_manager = ScheduleManager(db)
    user_schedules = schedule_manager.retrieve_schedule()
    return render_template('student_view_schedule.html', schedules=user_schedules)

@app.route('/generate_schedule', methods=['GET', 'POST'])
@login_required
def generate_schedule():
    if current_user.status == 'admin':
        return render_template('generate_schedule.html')
    else:
        return redirect(url_for('dashboard'))

@app.route('/generate_schedule_complete', methods=['POST'])
@login_required
def generate_schedule_complete():
    if current_user.status == 'admin':
        db = get_db()
        schedule_manager = ScheduleManager(db)

        # Retrieve data and schedule (example code)
        user_schedules = schedule_manager.retrieve_schedule()
        usernames, schedules = schedule_manager.get_usernames_and_schedules()
        schedule_manager.randomize_scheduling(usernames, schedules, schedule_manager)
        
        # Get the generated schedule
        generated_schedule = schedule_manager.get_schedule()

        return render_template('generated_schedule.html', schedule=generated_schedule)
    else:
        return redirect(url_for('dashboard'))
        
@app.route('/')
def home():
    return render_template('home.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

