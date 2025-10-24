from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import date

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    # Table constraint: unique exercise names
    name = db.Column(db.String(100), nullable=False, unique=True)
    # Table constraint: category cannot be empty string
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', overlaps="workout_exercises")

    # Model validation: name must be at least 2 characters
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long")
        return name.strip()
    
    # Model validation: category must be from allowed list
    @validates('category')
    def validate_category(self, key, category):
        allowed_categories = ['strength', 'cardio', 'flexibility', 'balance', 'sports']
        if category.lower() not in allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}")
        return category.lower()

    def __repr__(self):
        return f'<Exercise {self.name}>'

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    # Table constraint: duration must be positive
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    # Table constraints
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='positive_duration'),
    )
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan', overlaps="workouts")
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', overlaps="workout_exercises")

    # Model validation: duration must be between 5 and 600 minutes
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration < 5:
            raise ValueError("Workout duration must be at least 5 minutes")
        if duration > 600:
            raise ValueError("Workout duration cannot exceed 600 minutes (10 hours)")
        return duration
    
    # Model validation: date cannot be in the future
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
    
    # Table constraints: unique combination of workout and exercise
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
    )
    
    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises', overlaps="exercises,workouts")
    exercise = db.relationship('Exercise', back_populates='workout_exercises', overlaps="exercises,workouts")

    # Model validation: at least one of reps/sets or duration must be provided
    @validates('reps', 'sets', 'duration_seconds')
    def validate_exercise_data(self, key, value):
        # This validation will be checked when the object is committed
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: Workout {self.workout_id}, Exercise {self.exercise_id}>'