import json
import os

def get_student(student_id):
    path = f"students/{student_id}.json"
    if not os.path.exists(path):
        raise FileNotFoundError("Student not found")
    with open(path, 'r') as f:
        return json.load(f)

def save_student(student_data):
    path = f"students/{student_data['student_id']}.json"
    with open(path, 'w') as f:
        json.dump(student_data, f, indent=4)

def update_quiz_score(student_data, subject, new_score):
    scores = student_data['quiz_scores'].setdefault(subject, [])
    scores.append(new_score)

    avg = sum(scores) / len(scores)
    if avg >= 80:
        level = "strong"
    elif avg >= 60:
        level = "average"
    else:
        level = "needs improvement"
    student_data['performance'][subject] = level

