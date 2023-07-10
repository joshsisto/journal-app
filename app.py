from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from journal import create_journal_entry, guided_journal_entry, read_journal_entry, consolidate_files
from stats import create_stats_entry
from todo import manage_todo_list
from journal_bot import chatbot
from utilities import get_now, get_today
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'superdupersecret' 

# Configure the SQLite database. In a production application, you might use a server-based database like MySQL or PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'superSecure'  # Replace with your secret key
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        response = request.form.get('response', None)
        next_question = request.form.get('next_question', None)

        if response is not None:
            create_journal_entry(response)  # Call the function with the response from the form
            consolidate_files()  # Consolidate the files after saving the journal entry
            return jsonify({'result': 'Success!'})

        if next_question is not None:
            filename = f"{get_now()}.journal"
            goals_asked_file = f'./logs/{get_today()}/goals_asked.goals'
            questions = ["How are you feeling?", "Where are you writing this?", "Tell me about your day", "Anything else you would like to discuss?"]

            answer = request.form.get('answer')
            current_question = session.get('current_question', None)
            if current_question:
                with open(f'./logs/{get_today()}/' + filename, 'a') as file:
                    file.write(f"Question: {current_question}\n")
                    file.write(f"Response: {answer}\n")
                # If the goals question was asked, create the goals_asked.goals file and write the response
                if current_question == "What are your goals for the day?":
                    with open(goals_asked_file, 'w') as ga_file:
                        ga_file.write(f"Goals for the day: {answer}")
            session['current_question'] = None

            if datetime.now().hour < 18 and not os.path.exists(goals_asked_file):
                goals_question = "What are your goals for the day?"
                questions.append(goals_question)

            if not session.get('questions', []):
                session['questions'] = questions
            next_question = session['questions'].pop(0)
            session['current_question'] = next_question
            return jsonify({'result': 'Success!'})

    return render_template('home.html')

@app.route('/post', methods=['POST'])
def post():
    response = request.json.get('response', None)
    create_journal_entry(response)  # Call the function with the response from the form
    consolidate_files()  # Consolidate the files after saving the journal entry
    return jsonify({'result': 'Success!'})

def create_journal_entry(response):  # Add the response as a parameter
    try:
        filename = f"{get_now()}.journal"
        with open(f'./logs/{get_today()}/' + filename, 'w') as file:
            file.write(f"{datetime.now().ctime()}\n\n")  # Corrected this line
            file.write(f"{response}\n")  # Write the response from the form to the file
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    app.run(debug=True)

