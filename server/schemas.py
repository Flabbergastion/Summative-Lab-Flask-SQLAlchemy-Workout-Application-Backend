from marshmallow import Schema, fields, validates, ValidationError, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Exercise, Workout, WorkoutExercise
from datetime import date

class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        include_relationships = True
        load_instance = True
        
    # Schema validation: name length
    @validates('name')
    def validate_name(self, value, **kwargs):
        if len(value.strip()) < 2:
            raise ValidationError("Exercise name must be at least 2 characters long.")
        if len(value) > 100:
            raise ValidationError("Exercise name cannot exceed 100 characters.")
    
    # Schema validation: category must be valid
    @validates('category')
    def validate_category(self, value, **kwargs):
        allowed_categories = ['strength', 'cardio', 'flexibility', 'balance', 'sports']
        if value.lower() not in allowed_categories:
            raise ValidationError(f"Category must be one of: {', '.join(allowed_categories)}")

class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        include_relationships = True
        load_instance = True
    
    # Custom field for date validation
    date = fields.Date()
    
    # Schema validation: duration range
    @validates('duration_minutes')
    def validate_duration(self, value, **kwargs):
        if value < 5:
            raise ValidationError("Workout duration must be at least 5 minutes.")
        if value > 600:
            raise ValidationError("Workout duration cannot exceed 600 minutes.")
    
    # Schema validation: date cannot be in future
    @validates('date')
    def validate_date(self, value, **kwargs):
        if value and value > date.today():
            raise ValidationError("Workout date cannot be in the future.")

class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        include_relationships = True
        load_instance = True
    
    # Schema validation: at least one exercise metric must be provided
    @validates('reps')
    def validate_reps(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be a positive number.")
    
    @validates('sets')
    def validate_sets(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be a positive number.")
    
    @validates('duration_seconds')
    def validate_duration(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("Duration must be a positive number of seconds.")

# Nested schemas for detailed responses
class WorkoutDetailSchema(WorkoutSchema):
    """Workout schema with nested exercise details"""
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True)

class ExerciseDetailSchema(ExerciseSchema):
    """Exercise schema with nested workout details"""
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True)

# Initialize schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)

# For validation-only testing (without creating instances)
exercise_validation_schema = ExerciseSchema(load_instance=False)
workout_validation_schema = WorkoutSchema(load_instance=False)