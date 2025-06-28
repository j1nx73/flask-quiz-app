from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Admin credentials
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')

# Database Models
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)  # 'single_choice', 'multiple_choice', 'short_answer'
    difficulty = db.Column(db.String)
    correct_answer = db.Column(db.String)  # For short_answer
    explanation = db.Column(db.String)
    category = db.Column(db.String)  # New field for category
    options = db.relationship('Option', backref='question', lazy=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

# Function to populate the database with sample questions
def add_sample_questions():
    if Question.query.count() == 0:  # Only add if the database is empty
        # Single-choice question
        q1 = Question(text="What is 2+2?", type="single_choice", difficulty="easy", explanation="Basic arithmetic.", category="Math")
        db.session.add(q1)
        db.session.commit()
        db.session.add_all([
            Option(question_id=q1.id, text="3", is_correct=False),
            Option(question_id=q1.id, text="4", is_correct=True),
            Option(question_id=q1.id, text="5", is_correct=False)
        ])

        # Multiple-choice question
        q2 = Question(text="Which are prime numbers?", type="multiple_choice", difficulty="medium", explanation="Prime numbers have only two distinct factors: 1 and themselves.", category="Math")
        db.session.add(q2)
        db.session.commit()
        db.session.add_all([
            Option(question_id=q2.id, text="2", is_correct=True),
            Option(question_id=q2.id, text="3", is_correct=True),
            Option(question_id=q2.id, text="4", is_correct=False),
            Option(question_id=q2.id, text="5", is_correct=True)
        ])

        # Short-answer question
        q3 = Question(text="What is the capital of France?", type="short_answer", difficulty="easy", 
                     correct_answer="Paris", explanation="Paris is the capital city of France.", category="Geography")
        db.session.add(q3)
        db.session.commit()

        # More sample questions
        q4 = Question(text="Who wrote 'Hamlet'?", type="short_answer", difficulty="medium", correct_answer="Shakespeare", explanation="William Shakespeare wrote Hamlet.", category="Literature")
        db.session.add(q4)
        db.session.commit()
        q5 = Question(text="Which of the following are programming languages?", type="multiple_choice", difficulty="easy", explanation="Python, Java, and Ruby are programming languages.", category="Technology")
        db.session.add(q5)
        db.session.commit()
        db.session.add_all([
            Option(question_id=q5.id, text="Python", is_correct=True),
            Option(question_id=q5.id, text="Java", is_correct=True),
            Option(question_id=q5.id, text="Ruby", is_correct=True),
            Option(question_id=q5.id, text="HTML", is_correct=False)
        ])
        q6 = Question(text="What is the boiling point of water at sea level (°C)?", type="single_choice", difficulty="easy", explanation="Water boils at 100°C at sea level.", category="Science")
        db.session.add(q6)
        db.session.commit()
        db.session.add_all([
            Option(question_id=q6.id, text="90", is_correct=False),
            Option(question_id=q6.id, text="100", is_correct=True),
            Option(question_id=q6.id, text="110", is_correct=False)
        ])
        db.session.commit()

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    num_questions = int(request.form.get('num_questions', 10))
    questions = Question.query.order_by(db.func.random()).limit(num_questions).all()
    session['question_ids'] = [q.id for q in questions]
    session['current_index'] = 0
    session['answers'] = []
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'question_ids' not in session:
        return redirect(url_for('home'))
    index = session['current_index']
    if index >= len(session['question_ids']):
        return redirect(url_for('results'))
    question_id = session['question_ids'][index]
    question = Question.query.get(question_id)

    if request.method == 'POST':
        if question.type == 'short_answer':
            user_answer = request.form.get('answer', '').strip().lower()
            is_correct = user_answer == question.correct_answer.strip().lower()
        else:  # single_choice or multiple_choice
            selected_options = request.form.getlist('options')
            correct_options = [str(o.id) for o in question.options if o.is_correct]
            if question.type == 'single_choice':
                is_correct = len(selected_options) == 1 and selected_options[0] in correct_options
            else:  # multiple_choice
                is_correct = set(selected_options) == set(correct_options)
        session['answers'].append({'question_id': question_id, 'is_correct': is_correct})
        session['current_index'] += 1
        return redirect(url_for('question'))

    return render_template('question.html', question=question, index=index + 1, total=len(session['question_ids']))

@app.route('/results')
def results():
    if 'answers' not in session:
        return redirect(url_for('home'))
    answers = session['answers']
    score = sum(1 for a in answers if a['is_correct'])
    total = len(answers)
    incorrect_questions = [Question.query.get(a['question_id']) for a in answers if not a['is_correct']]
    session.clear()  # Clear session after quiz
    return render_template('results.html', score=score, total=total, incorrect_questions=incorrect_questions)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid credentials.'
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    selected_category = request.args.get('category', '')
    if selected_category:
        questions = Question.query.filter_by(category=selected_category).all()
    else:
        questions = Question.query.all()
    categories = sorted(set(q.category for q in Question.query.all() if q.category))
    return render_template('admin_dashboard.html', questions=questions, categories=categories, selected_category=selected_category)

@app.route('/admin/add', methods=['GET', 'POST'])
@admin_required
def admin_add_question():
    error = None
    if request.method == 'POST':
        text = request.form.get('text')
        qtype = request.form.get('type')
        difficulty = request.form.get('difficulty')
        category = request.form.get('category')
        explanation = request.form.get('explanation')
        correct_answer = request.form.get('correct_answer') if qtype == 'short_answer' else None
        # Validate
        if not text or not qtype or not category:
            error = 'Please fill in all required fields.'
        else:
            question = Question(text=text, type=qtype, difficulty=difficulty, category=category, explanation=explanation, correct_answer=correct_answer)
            db.session.add(question)
            db.session.commit()
            if qtype in ['single_choice', 'multiple_choice']:
                for i in range(1, 5):
                    opt_text = request.form.get(f'option_text_{i}')
                    opt_correct = request.form.get(f'option_correct_{i}')
                    if opt_text:
                        option = Option(question_id=question.id, text=opt_text, is_correct=bool(opt_correct))
                        db.session.add(option)
                db.session.commit()
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_question.html', error=error)

@app.route('/health')
def health_check():
    """Health check endpoint for production monitoring."""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'database': 'connected'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

# Initialize database
with app.app_context():
    db.create_all()
    add_sample_questions()

if __name__ == '__main__':
    app.run(debug=True, port=5002)