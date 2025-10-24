from marshmallow import fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Exercise, Workout, WorkoutExercise, ALLOWED_CATEGORIES
from datetime import date

class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
        
    @validates('name')
    def validate_name(self, value, **kwargs):
        value = value.strip()
        if len(value) < 2 or len(value) > 100:
            raise ValidationError("Exercise name must be 2-100 characters long.")
    
    @validates('category')
    def validate_category(self, value, **kwargs):
        if value.lower() not in ALLOWED_CATEGORIES:
            raise ValidationError(f"Category must be one of: {', '.join(ALLOWED_CATEGORIES)}")

class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True
    
    @validates('duration_minutes')
    def validate_duration(self, value, **kwargs):
        if not (5 <= value <= 600):
            raise ValidationError("Workout duration must be between 5 and 600 minutes.")
    
    @validates('date')
    def validate_date(self, value, **kwargs):
        if value and value > date.today():
            raise ValidationError("Workout date cannot be in the future.")

class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
    
    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive_numbers(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("Value must be a positive number.")

# Schema instances - simplified
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()  
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

# Detail schemas with nested relationships
class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True)

class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True)

workout_detail_schema = WorkoutDetailSchema()
exercise_detail_schema = ExerciseDetailSchema()