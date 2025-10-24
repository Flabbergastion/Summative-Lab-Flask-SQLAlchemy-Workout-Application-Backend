# Workout Tracker API

## Project Description

A complete Flask-based REST API for tracking workouts and exercises, built with SQLAlchemy ORM and Marshmallow for data validation and serialization. This application allows personal trainers to manage workouts and exercises with comprehensive relationship tracking, including sets, reps, and duration data.

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

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | **List all workouts** - Returns array of all workouts with basic info |
| GET | `/workouts/<id>` | **Get single workout** - Returns detailed workout with associated exercises and performance data |
| POST | `/workouts` | **Create workout** - Creates new workout. Requires `duration_minutes`, optional `date` and `notes` |
| DELETE | `/workouts/<id>` | **Delete workout** - Removes workout and all associated exercise relationships |
| GET | `/exercises` | **List all exercises** - Returns array of all available exercises |
| GET | `/exercises/<id>` | **Get single exercise** - Returns detailed exercise with associated workouts |
| POST | `/exercises` | **Create exercise** - Creates new exercise. Requires `name`, `category`, optional `equipment_needed` |
| DELETE | `/exercises/<id>` | **Delete exercise** - Removes exercise and all associated workout relationships |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | **Add exercise to workout** - Links an exercise to a workout with performance metrics (reps, sets, duration_seconds) |

### Example Requests

**Create a workout:**
```bash
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"duration_minutes": 45, "notes": "Upper body strength training"}'


**Create an exercise:**
```bash
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Pull-ups", "category": "strength", "equipment_needed": true}'


**Add exercise to workout:**
```bash
curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 10, "sets": 3}'


## Installation Instructions

### Prerequisites
- Python 3.8+
- Git

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/Flabbergastion/Summative-Lab-Flask-SQLAlchemy-Workout-Application-Backend.git
cd Summative-Lab-Flask-SQLAlchemy-Workout-Application-Backend


2. **Install dependencies**
```bash
pipenv install
pipenv shell


3. **Navigate to server directory and set up database**
```bash
cd server
flask db upgrade


4. **Seed the database with example data**
```bash
python seed.py


## Run Instructions

**Start the Flask development server:**
```bash
cd server
python app.py


The API will be available at `http://localhost:5555`

**Alternative Flask run command:**
```bash
flask run --port=5555


## Testing

Run the included test script to verify API functionality:
```bash
# Start the server in one terminal
cd server
python app.py

# Run tests in another terminal
python test_api.py


## Project Structure


├── server/
│   ├── app.py              # Flask application and routes
│   ├── models.py           # SQLAlchemy models with validations
│   ├── schemas.py          # Marshmallow schemas for serialization
│   ├── seed.py             # Database seeding script with example data
│   ├── migrations/         # Flask-Migrate database migration files
│   └── instance/           # SQLite database files (created after setup)
├── test_api.py             # API test script 
├── Pipfile                 # Project dependencies
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation


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
