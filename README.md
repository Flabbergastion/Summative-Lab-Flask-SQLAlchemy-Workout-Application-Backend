# Workout Tracker API

A complete Flask-based REST API for tracking workouts and exercises, built with SQLAlchemy ORM and Marshmallow for data validation and serialization.

## Features

- **Complete CRUD Operations**: Create, read, and delete workouts and exercises
- **Relationship Management**: Link exercises to workouts with sets, reps, and duration tracking
- **Comprehensive Validations**: Multi-layer validation at database, model, and schema levels
- **RESTful API Design**: Following REST conventions and best practices
- **Data Serialization**: JSON serialization with nested relationships

## Database Schema

### Models

#### Exercise
- `id`: Primary key (integer)
- `name`: Exercise name (string, unique, 2-100 characters)
- `category`: Exercise category (strength, cardio, flexibility, balance, sports)
- `equipment_needed`: Boolean flag for equipment requirement

#### Workout
- `id`: Primary key (integer)
- `date`: Workout date (cannot be in future, defaults to today)
- `duration_minutes`: Workout duration (5-600 minutes)
- `notes`: Optional text notes

#### WorkoutExercise (Join Table)
- `id`: Primary key (integer)
- `workout_id`: Foreign key to Workout
- `exercise_id`: Foreign key to Exercise
- `reps`: Number of repetitions (optional, positive integer)
- `sets`: Number of sets (optional, positive integer)
- `duration_seconds`: Exercise duration in seconds (optional, positive integer)

### Relationships
- A Workout has many Exercises through WorkoutExercises
- An Exercise has many Workouts through WorkoutExercises
- A WorkoutExercise belongs to both a Workout and an Exercise

## Validations

### Table Constraints
1. **Exercise names must be unique**
2. **Workout duration must be positive** (CHECK constraint)
3. **Unique workout-exercise combinations** (prevents duplicates)

### Model Validations
1. **Exercise name**: Minimum 2 characters, valid category from allowed list
2. **Workout duration**: 5-600 minutes range
3. **Workout date**: Cannot be in the future

### Schema Validations
1. **Exercise name**: Length validation and category validation
2. **Workout duration**: Range validation
3. **WorkoutExercise metrics**: Positive number validation for reps, sets, and duration

## API Endpoints

### Workouts

#### GET /workouts
List all workouts
```json
Response: [
  {
    "id": 1,
    "date": "2025-10-17",
    "duration_minutes": 45,
    "notes": "Great upper body workout",
    "exercises": [1, 3],
    "workout_exercises": [1, 2]
  }
]
```

#### GET /workouts/<id>
Get single workout with exercise details
```json
Response: {
  "id": 1,
  "date": "2025-10-17",
  "duration_minutes": 45,
  "notes": "Great upper body workout",
  "workout_exercises": [
    {
      "id": 1,
      "exercise_id": 1,
      "reps": 15,
      "sets": 3,
      "duration_seconds": null
    }
  ]
}
```

#### POST /workouts
Create a new workout
```json
Request: {
  "duration_minutes": 30,
  "notes": "Morning cardio session"
}
Response: 201 Created with workout object
```

#### DELETE /workouts/<id>
Delete a workout (cascades to WorkoutExercises)
```json
Response: {"message": "Workout {id} deleted successfully"}
```

### Exercises

#### GET /exercises
List all exercises
```json
Response: [
  {
    "id": 1,
    "name": "Push-ups",
    "category": "strength",
    "equipment_needed": false,
    "workouts": [1, 3],
    "workout_exercises": [1, 6]
  }
]
```

#### GET /exercises/<id>
Get single exercise with workout details
```json
Response: {
  "id": 1,
  "name": "Push-ups",
  "category": "strength",
  "equipment_needed": false,
  "workout_exercises": [
    {
      "id": 1,
      "workout_id": 1,
      "reps": 15,
      "sets": 3
    }
  ]
}
```

#### POST /exercises
Create a new exercise
```json
Request: {
  "name": "Burpees",
  "category": "cardio",
  "equipment_needed": false
}
Response: 201 Created with exercise object
```

#### DELETE /exercises/<id>
Delete an exercise (cascades to WorkoutExercises)
```json
Response: {"message": "Exercise {id} deleted successfully"}
```

### Workout-Exercise Relationships

#### POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Add an exercise to a workout with performance metrics
```json
Request: {
  "reps": 12,
  "sets": 3,
  "duration_seconds": null
}
Response: 201 Created with WorkoutExercise object
```

## Setup and Installation

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd workout-tracker-api
```

2. **Install dependencies using pipenv**
```bash
pipenv install
pipenv shell
```

3. **Set up the database**
```bash
cd server
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

4. **Seed the database with sample data**
```bash
python seed.py
```

5. **Run the development server**
```bash
python app.py
```

The API will be available at `http://localhost:5555`

## Usage Examples

### Create a workout
```bash
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"duration_minutes": 45, "notes": "Upper body strength training"}'
```

### Create an exercise
```bash
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Pull-ups", "category": "strength", "equipment_needed": true}'
```

### Add exercise to workout
```bash
curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 10, "sets": 3}'
```

## Project Structure

```
├── server/
│   ├── app.py              # Flask application and routes
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Marshmallow schemas
│   ├── seed.py             # Database seeding script
│   ├── migrations/         # Flask-Migrate files
│   └── app.db              # SQLite database (created after setup)
├── Pipfile                 # Dependencies
└── README.md              # This file
```

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Migrate**: Database migrations
- **Marshmallow**: Data serialization and validation
- **SQLite**: Database (development)

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Validation errors with detailed messages
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server errors

Example validation error response:
```json
{
  "errors": {
    "duration_minutes": ["Workout duration must be at least 5 minutes."],
    "category": ["Category must be one of: strength, cardio, flexibility, balance, sports"]
  }
}
```