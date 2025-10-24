#!/usr/bin/env python3
"""
Simple test script to demonstrate API functionality
Run with: python test_api.py (while Flask server is running)
"""

import requests
import json

BASE_URL = "http://localhost:5555"

def test_get_workouts():
    """Test GET /workouts endpoint"""
    print("Testing GET /workouts...")
    response = requests.get(f"{BASE_URL}/workouts")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        workouts = response.json()
        print(f"Found {len(workouts)} workouts")
        return True
    else:
        print(f"Error: {response.json()}")
        return False

def test_get_exercises():
    """Test GET /exercises endpoint"""
    print("\nTesting GET /exercises...")
    response = requests.get(f"{BASE_URL}/exercises")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        exercises = response.json()
        print(f"Found {len(exercises)} exercises")
        return True
    else:
        print(f"Error: {response.json()}")
        return False

def test_create_workout():
    """Test POST /workouts endpoint"""
    print("\nTesting POST /workouts...")
    new_workout = {
        "duration_minutes": 35,
        "notes": "Test workout from API test"
    }
    
    response = requests.post(
        f"{BASE_URL}/workouts",
        headers={"Content-Type": "application/json"},
        json=new_workout
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        workout = response.json()
        print(f"Created workout with ID: {workout['id']}")
        return workout['id']
    else:
        print(f"Error: {response.json()}")
        return None

def test_create_exercise():
    """Test POST /exercises endpoint"""
    print("\nTesting POST /exercises...")
    new_exercise = {
        "name": "Test Exercise",
        "category": "strength",
        "equipment_needed": False
    }
    
    response = requests.post(
        f"{BASE_URL}/exercises",
        headers={"Content-Type": "application/json"},
        json=new_exercise
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        exercise = response.json()
        print(f"Created exercise with ID: {exercise['id']}")
        return exercise['id']
    else:
        print(f"Error: {response.json()}")
        return None

def test_validation_error():
    """Test validation errors"""
    print("\nTesting validation error...")
    invalid_workout = {
        "duration_minutes": 2,  # Too short, should fail
        "notes": "This should fail validation"
    }
    
    response = requests.post(
        f"{BASE_URL}/workouts",
        headers={"Content-Type": "application/json"},
        json=invalid_workout
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        errors = response.json()
        print(f"Validation error (expected): {errors}")
        return True
    else:
        print("Unexpected response - validation should have failed")
        return False

if __name__ == "__main__":
    print("🧪 Running API Tests...")
    print("Make sure Flask server is running on http://localhost:5555")
    print("-" * 50)
    
    try:
        # Run tests
        test_get_workouts()
        test_get_exercises()
        test_create_workout()
        test_create_exercise()
        test_validation_error()
        
        print("\n✅ API tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Flask server.")
        print("Please start the server with: python app.py")
    except Exception as e:
        print(f"❌ Test error: {e}")