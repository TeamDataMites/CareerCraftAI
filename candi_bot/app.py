from flask import Flask, flash, redirect, request, render_template, session, jsonify, url_for
from utils import extract_text_from_pdf, check_correct, allowed_file, generate_questions, insert_score
import os
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Set the secret key

CORS(app)

# MongoDB setup
# MONGO_URI = os.getenv('MONGO_URI')
# client = MongoClient(MONGO_URI)
# db = client['your_database_name']
# scores_collection = db['scores']

predefined_questions = [
    "What is your full name?",
    "What university did you attend?",
    "What is your current GPA?"
]

hr_questions = [
    "What is your expected salary in LKR?",
    "When is the possible join date for you?",
    "Do you prefer WFH, WFO or hybrid?",
    "What are your preferred working hours?"
]

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        pdf_text = extract_text_from_pdf(file)
        if pdf_text:
            generated_questions = generate_questions(pdf_text)
            if isinstance(generated_questions, dict) and "Error" in generated_questions:
                flash('Error: Unable to generate questions. Please try again later.')
                return redirect(request.url)

            session['cv_text'] = pdf_text  # Store CV text in session
            session['questions'] = predefined_questions + generated_questions  # Combine predefined and generated questions
            session['current_question_index'] = 0
            session['user_answers'] = {}
            return redirect(url_for('chat'))
        else:
            flash('Error: Unable to extract text from PDF')
            return redirect(request.url)
    else:
        flash('Invalid file type. Please upload a PDF.')
        return redirect(request.url)

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    if 'questions' not in session or 'current_question_index' not in session:
        return jsonify({'error': 'Session expired. Please upload the PDF again.'}), 400

    current_index = session['current_question_index']
    questions = session['questions']

    if current_index < len(questions):
        current_question = questions[current_index]
        return jsonify({'question': current_question})
    else:
        return jsonify({'error': 'No more questions.'}), 400
    

@app.route('/get_hr_question', methods=['GET'])
def get_question2():
    if 'questions2' not in session or 'current_question_index' not in session:
        return jsonify({'error': 'Session expired. Please upload the PDF again.'}), 400

    current_index = session['current_question_index']
    questions2 = session['questions2']

    if current_index < len(questions2):
        current_question = questions2[current_index]
        return jsonify({'question': current_question})
    else:
        return jsonify({'error': 'No more questions.'}), 400

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'questions' not in session or 'current_question_index' not in session:
        return jsonify({'error': 'Session expired. Please upload the PDF again.'}), 400

    current_index = session['current_question_index']
    questions = session['questions']

    if current_index >= len(questions):
        return jsonify({'error': 'No more questions.'}), 400

    answer = request.form.get('answer')
    if not answer:
        return jsonify({'error': 'Answer cannot be empty.'}), 400

    question_type = 'generated' if current_index >= len(predefined_questions) else 'predefined'
    session['user_answers'][questions[current_index]] = {'answer': answer, 'type': question_type}
    session['current_question_index'] += 1

    print("lenth", len(session['questions']))
    print("session['current_question_index']", session['current_question_index'])

    # Check if all questions are answered
    if session['current_question_index'] >= len(session['questions']):
        return redirect(url_for('ask_hr_questions'))

    return jsonify({'success': 'Answer submitted successfully.'})

@app.route('/ask_hr_questions')
def ask_hr_questions():
    session['current_question_index'] = 0  # Reset current question index for HR questions
    session['questions2'] = hr_questions  # Set HR questions for session
    session['user_answers2'] = {}  # Initialize user answers for HR questions
    return redirect(url_for('chat'))


@app.route('/submit_hr_answers', methods=['POST'])
def submit_hr_answers():
    if 'questions2' not in session or 'current_question_index' not in session:
        return jsonify({'error': 'Session expired. Please upload the PDF again.'}), 400

    current_index = session['current_question_index']
    questions = session['questions2']

    if current_index >= len(questions):
        return jsonify({'error': 'No more questions.'}), 400

    answer = request.form.get('answer')
    if not answer:
        return jsonify({'error': 'Answer cannot be empty.'}), 400

    session['user_answers2'][questions[current_index]] = {'answer': answer}
    session['current_question_index'] += 1

    print("lenthof-HR", len(session['questions2']))
    print("session['current_question_index']-HR", session['current_question_index'])

    # Check if all HR questions are answered
    if session['current_question_index'] >= len(session['questions2']):
        cv_text = session['cv_text']
        hr_answers = session['user_answers2']

        # Redirect to show_results after all HR questions are answered
        return redirect(url_for('show_results'))

    return jsonify({'success': 'Answer submitted successfully.'})


@app.route('/results')
def show_results():
    if 'cv_text' not in session or 'user_answers' not in session:
        flash('Session expired. Please upload the PDF again.')
        return redirect('/')

    cv_text = session['cv_text']
    user_answers = session['user_answers']
    questions = session['questions']
    user_answers2 = session['user_answers2']
    questions2 = session['questions2']

    print("user_answers--", user_answers2)
    print("questions--", questions2)

    correct_count = 0
    results = []

    for question in questions:
        print(" user_answers.get(question)--", user_answers.get(question))
        answer_data = user_answers.get(question)
        if answer_data:
            answer = answer_data['answer']
            print(" answer_data['type']--", answer_data.get('type'))
            is_generated = answer_data.get('type') == 'generated'
            is_correct = check_correct(question, answer, cv_text, generated=is_generated)
            results.append((question, answer, is_correct))
            if is_correct:
                correct_count += 1

    total_questions = len(questions)
    score = (correct_count / total_questions) * 100

    # Insert score into MongoDB
    insert_score(score, cv_text, user_answers2)

    return render_template('results.html', score=score, results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
