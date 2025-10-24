from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import *
from schemas import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Error handler decorator for cleaner code
def handle_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return jsonify({"errors": e.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    wrapper.__name__ = f.__name__
    return wrapper

# Workout Routes
@app.route('/workouts', methods=['GET'])
@handle_errors
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts))

@app.route('/workouts/<int:id>', methods=['GET'])
@handle_errors
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return jsonify(workout_detail_schema.dump(workout))

@app.route('/workouts', methods=['POST'])
@handle_errors
def create_workout():
    workout_data = workout_schema.load(request.json)
    db.session.add(workout_data)
    db.session.commit()
    return jsonify(workout_schema.dump(workout_data)), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
@handle_errors
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {id} deleted successfully"})

# Exercise Routes
@app.route('/exercises', methods=['GET'])
@handle_errors
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises))

@app.route('/exercises/<int:id>', methods=['GET'])
@handle_errors
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return jsonify(exercise_detail_schema.dump(exercise))

@app.route('/exercises', methods=['POST'])
@handle_errors
def create_exercise():
    exercise_data = exercise_schema.load(request.json)
    db.session.add(exercise_data)
    db.session.commit()
    return jsonify(exercise_schema.dump(exercise_data)), 201

@app.route('/exercises/<int:id>', methods=['DELETE'])
@handle_errors
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {id} deleted successfully"})

# WorkoutExercise Routes
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
@handle_errors
def add_exercise_to_workout(workout_id, exercise_id):
    # Verify resources exist and no duplicate
    Workout.query.get_or_404(workout_id)
    Exercise.query.get_or_404(exercise_id)
    
    if WorkoutExercise.query.filter_by(workout_id=workout_id, exercise_id=exercise_id).first():
        return jsonify({"error": "Exercise already added to this workout"}), 400
    
    # Prepare data
    data = request.json or {}
    data.update({'workout_id': workout_id, 'exercise_id': exercise_id})
    
    # Validate at least one metric is provided
    if not any([data.get('reps'), data.get('sets'), data.get('duration_seconds')]):
        return jsonify({"error": "At least one of reps, sets, or duration_seconds must be provided"}), 400
    
    workout_exercise = workout_exercise_schema.load(data)
    db.session.add(workout_exercise)
    db.session.commit()
    
    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)