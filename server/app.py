from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import *
from schemas import (
    exercise_schema, exercises_schema, exercise_detail_schema,
    workout_schema, workouts_schema, workout_detail_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Workout Routes

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """List all workouts"""
    try:
        workouts = Workout.query.all()
        return jsonify(workouts_schema.dump(workouts)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    """Show a single workout with its associated exercises"""
    try:
        workout = Workout.query.get_or_404(id)
        return jsonify(workout_detail_schema.dump(workout)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/workouts', methods=['POST'])
def create_workout():
    """Create a workout"""
    try:
        workout_data = workout_schema.load(request.json)
        db.session.add(workout_data)
        db.session.commit()
        return jsonify(workout_schema.dump(workout_data)), 201
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """Delete a workout (includes cascade delete of associated WorkoutExercises)"""
    try:
        workout = Workout.query.get_or_404(id)
        db.session.delete(workout)
        db.session.commit()
        return jsonify({"message": f"Workout {id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Exercise Routes

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """List all exercises"""
    try:
        exercises = Exercise.query.all()
        return jsonify(exercises_schema.dump(exercises)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    """Show an exercise and associated workouts"""
    try:
        exercise = Exercise.query.get_or_404(id)
        return jsonify(exercise_detail_schema.dump(exercise)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/exercises', methods=['POST'])
def create_exercise():
    """Create an exercise"""
    try:
        exercise_data = exercise_schema.load(request.json)
        db.session.add(exercise_data)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise_data)), 201
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """Delete an exercise (includes cascade delete of associated WorkoutExercises)"""
    try:
        exercise = Exercise.query.get_or_404(id)
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({"message": f"Exercise {id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# WorkoutExercise Routes

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """Add an exercise to a workout, including reps/sets/duration"""
    try:
        # Verify workout and exercise exist
        workout = Workout.query.get_or_404(workout_id)
        exercise = Exercise.query.get_or_404(exercise_id)
        
        # Check if this combination already exists
        existing = WorkoutExercise.query.filter_by(
            workout_id=workout_id, 
            exercise_id=exercise_id
        ).first()
        
        if existing:
            return jsonify({"error": "Exercise already added to this workout"}), 400
        
        # Create new WorkoutExercise with data from request
        workout_exercise_data = request.json or {}
        workout_exercise_data['workout_id'] = workout_id
        workout_exercise_data['exercise_id'] = exercise_id
        
        # Validate that at least one metric is provided
        if not any([workout_exercise_data.get('reps'), 
                   workout_exercise_data.get('sets'), 
                   workout_exercise_data.get('duration_seconds')]):
            return jsonify({"error": "At least one of reps, sets, or duration_seconds must be provided"}), 400
        
        workout_exercise = workout_exercise_schema.load(workout_exercise_data)
        db.session.add(workout_exercise)
        db.session.commit()
        
        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201
        
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)