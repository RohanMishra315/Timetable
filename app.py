from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
db = SQLAlchemy(app)

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50))
    time = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    teacher = db.Column(db.String(100))

    def __init__(self, day, time, subject, teacher):
        self.day = day
        self.time = time
        self.subject = subject
        self.teacher = teacher

@app.route('/add_timetable', methods=['POST'])
def add_timetable():
    data = request.json
    day = data.get('day')
    time = data.get('time')
    subject = data.get('subject')
    teacher = data.get('teacher')
    if not all([day, time, subject, teacher]):
        return jsonify({'error': 'Missing fields'}), 400
    new_timetable = Timetable(day=day, time=time, subject=subject, teacher=teacher)
    try:
        db.session.add(new_timetable)
        db.session.commit()
        return jsonify({'message': 'Timetable entry added successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Duplicate entry'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/generate_timetable', methods=['GET'])
def generate_timetable():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    times = ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM']
    subjects = ['Math', 'Science', 'History', 'English', 'Art']
    teachers = ['Mr. Smith', 'Ms. Johnson', 'Mr. Brown', 'Ms. Davis', 'Mr. Wilson']

    generated_timetable = []

    for day in days:
        for time in times:
            subject = random.choice(subjects)
            teacher = random.choice(teachers)
            generated_timetable.append({
                'day': day,
                'time': time,
                'subject': subject,
                'teacher': teacher
            })

    return jsonify(generated_timetable)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
