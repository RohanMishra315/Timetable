from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
db = SQLAlchemy(app)

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON)

    def __init__(self, day, time, subject, ):
        self.data = {
            'day': day,
            'time': time,
            'subject': subject,
            
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


@app.route('/add_timetable', methods=['POST'])
def add_timetable():
    data = request.json
    day = data.get('day')
    time = data.get('time')
    subject = data.get('subject')
    if not all([day, time, subject,]):
        return jsonify({'error': 'Missing fields'}), 400
    new_timetable = Timetable(day=day, time=time, subject=subject, )
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

    generated_timetable = []

    for day in days:
        for time in times:
            subject = random.choice(subjects)
            generated_timetable.append({
                'day': day,
                'time': time,
                'subject': subject,
            
            })

    return jsonify(generated_timetable)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)