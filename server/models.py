from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import date

db = SQLAlchemy()

# Define allowed categories as a constant
ALLOWED_CATEGORIES = ['strength', 'cardio', 'flexibility', 'balance', 'sports']

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)
    
    # Simplified relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long")
        return name.strip()
    
    @validates('category')
    def validate_category(self, key, category):
        if category.lower() not in ALLOWED_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(ALLOWED_CATEGORIES)}")
        return category.lower()

    def __repr__(self):
        return f'<Exercise {self.name}>'

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='positive_duration'),
    )
    
    # Simplified relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration < 5 or duration > 600:
            raise ValueError("Workout duration must be between 5 and 600 minutes")
        return duration
    
    @validates('date')
    def validate_date(self, key, workout_date):
        if workout_date and workout_date > date.today():
            raise ValueError("Workout date cannot be in the future")
        return workout_date

    def __repr__(self):
        return f'<Workout {self.id} on {self.date}>'

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
    )
    
    # Simplified relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: Workout {self.workout_id}, Exercise {self.exercise_id}>'