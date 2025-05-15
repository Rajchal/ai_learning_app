from flask import Flask, request, jsonify
import subprocess
from utils import get_student, save_student, update_quiz_score

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    student_id = data['student_id']
    user_input = data['message']

    student = get_student(student_id)

    # Build context for Ollama
    context = f"""
Student Name: {student['name']}
Performance Summary: {student['performance']}
Quiz Scores: {student['quiz_scores']}
"""

    full_prompt = context + f"\nUser: {user_input}\nAssistant:"

    # Run Ollama
    result = subprocess.run(
        ['ollama', 'run', 'llama2', full_prompt],
        capture_output=True, text=True
    )
    response = result.stdout.strip()

    # Save chat
    student['chat_history'].append({"user": user_input, "assistant": response})
    save_student(student)

    return jsonify({"response": response})


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    student_id = data['student_id']
    subject = data['subject']
    score = data['score']

    student = get_student(student_id)
    update_quiz_score(student, subject, score)
    save_student(student)

    return jsonify({"message": "Score updated", "performance": student['performance']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

