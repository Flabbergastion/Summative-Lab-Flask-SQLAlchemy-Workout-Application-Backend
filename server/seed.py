#!/usr/bin/env python3

from app import app
from models import *
from datetime import date, timedelta

with app.app_context():
    
    # Clear existing data
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()
    
    # Create sample exercises
    print("Creating exercises...")
    exercises = [
        Exercise(name="Push-ups", category="strength", equipment_needed=False),
        Exercise(name="Squats", category="strength", equipment_needed=False),
        Exercise(name="Bench Press", category="strength", equipment_needed=True),
        Exercise(name="Running", category="cardio", equipment_needed=False),
        Exercise(name="Deadlifts", category="strength", equipment_needed=True),
        Exercise(name="Yoga Flow", category="flexibility", equipment_needed=False),
        Exercise(name="Bicep Curls", category="strength", equipment_needed=True),
        Exercise(name="Jumping Jacks", category="cardio", equipment_needed=False),
    ]
    
    for exercise in exercises:
        db.session.add(exercise)
    
    db.session.commit()
    print(f"Created {len(exercises)} exercises")
    
    # Create sample workouts
    print("Creating workouts...")
    workouts = [
        Workout(
            date=date.today() - timedelta(days=7),
            duration_minutes=45,
            notes="Great upper body workout"
        ),
        Workout(
            date=date.today() - timedelta(days=5),
            duration_minutes=30,
            notes="Quick cardio session"
        ),
        Workout(
            date=date.today() - timedelta(days=3),
            duration_minutes=60,
            notes="Full body strength training"
        ),
        Workout(
            date=date.today() - timedelta(days=1),
            duration_minutes=25,
            notes="Recovery and flexibility"
        )
    ]
    
    for workout in workouts:
        db.session.add(workout)
    
    db.session.commit()
    print(f"Created {len(workouts)} workouts")
    
    # Create workout-exercise relationships
    print("Creating workout-exercise relationships...")
    
    # Get exercises and workouts from database
    pushups = Exercise.query.filter_by(name="Push-ups").first()
    squats = Exercise.query.filter_by(name="Squats").first()
    bench_press = Exercise.query.filter_by(name="Bench Press").first()
    running = Exercise.query.filter_by(name="Running").first()
    deadlifts = Exercise.query.filter_by(name="Deadlifts").first()
    yoga = Exercise.query.filter_by(name="Yoga Flow").first()
    
    workout1 = workouts[0]  # Upper body workout
    workout2 = workouts[1]  # Cardio session
    workout3 = workouts[2]  # Full body strength
    workout4 = workouts[3]  # Recovery
    
    workout_exercises = [
        # Workout 1 - Upper body
        WorkoutExercise(workout_id=workout1.id, exercise_id=pushups.id, reps=15, sets=3),
        WorkoutExercise(workout_id=workout1.id, exercise_id=bench_press.id, reps=10, sets=4),
        
        # Workout 2 - Cardio
        WorkoutExercise(workout_id=workout2.id, exercise_id=running.id, duration_seconds=1800),  # 30 minutes
        
        # Workout 3 - Full body strength  
        WorkoutExercise(workout_id=workout3.id, exercise_id=squats.id, reps=12, sets=4),
        WorkoutExercise(workout_id=workout3.id, exercise_id=deadlifts.id, reps=8, sets=3),
        WorkoutExercise(workout_id=workout3.id, exercise_id=pushups.id, reps=20, sets=2),
        
        # Workout 4 - Recovery
        WorkoutExercise(workout_id=workout4.id, exercise_id=yoga.id, duration_seconds=1500),  # 25 minutes
    ]
    
    for workout_exercise in workout_exercises:
        db.session.add(workout_exercise)
    
    db.session.commit()
    print(f"Created {len(workout_exercises)} workout-exercise relationships")
    
    print("Seed data creation complete!")
    
    # Verify relationships work
    print("\nVerifying relationships...")
    first_workout = Workout.query.first()
    print(f"First workout has {len(first_workout.workout_exercises)} exercise relationships")
    
    first_exercise = Exercise.query.first()
    print(f"First exercise appears in {len(first_exercise.workout_exercises)} workout relationships")