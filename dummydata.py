import random
import csv
from typing import List, Dict

def generate_dummy_data(num_entries: int) -> List[Dict]:
    genders = ['Male', 'Female']
    body_goals = ['lose weight', 'gain muscle', 'increase strength']
    problem_areas = ['weak_chest', 'weak_back', 'big_belly', 'small_arms', 'small_legs']
    fitness_levels = ['beginner', 'intermediate', 'advanced']

    data = []

    for _ in range(num_entries):
        gender = random.choice(genders)
        age = generate_age()
        height = random.randint(150, 200)
        weight = calculate_weight(height, age, gender)
        
        fitness_level = determine_fitness_level(age)
        body_goal = determine_body_goal(age, weight, height)
        workout_days = determine_workout_days(age, fitness_level)
        selected_problems = select_problem_areas(body_goal, age, fitness_level)

        entry = {
            'Gender': gender,
            'Age': age,
            'BodyGoal': body_goal,
            'ProblemAreas': selected_problems,
            'Height_cm': height,
            'Weight_kg': weight,
            'FitnessLevel': fitness_level,
            'WorkoutDaysPerWeek': workout_days
        }

        schedule = generate_workout_schedule(workout_days, selected_problems, fitness_level, body_goal)
        entry.update(schedule)

        data.append(entry)

    return data

def generate_age():
    age_ranges = [
        (18, 25, 0.35),  # 35% chance for 18-25
        (26, 35, 0.30),  # 30% chance for 26-35
        (36, 45, 0.20),  # 20% chance for 36-45
        (46, 60, 0.10),  # 10% chance for 46-60
        (61, 90, 0.05)   # 5% chance for 61-90
    ]
    
    selected_range = random.choices(age_ranges, weights=[r[2] for r in age_ranges])[0]
    return random.randint(selected_range[0], selected_range[1])

def calculate_weight(height: int, age: int, gender: str) -> int:
    base_weight = (height - 100) * 0.9
    age_factor = (age - 30) * 0.1 if age > 30 else 0
    gender_factor = 5 if gender == 'Male' else -5
    variation = random.uniform(-5, 5)
    return max(40, min(150, int(base_weight + age_factor + gender_factor + variation)))

def determine_fitness_level(age: int) -> str:
    if age < 30:
        return random.choices(['beginner', 'intermediate', 'advanced'], weights=[0.4, 0.4, 0.2])[0]
    elif age < 50:
        return random.choices(['beginner', 'intermediate', 'advanced'], weights=[0.3, 0.5, 0.2])[0]
    else:
        return random.choices(['beginner', 'intermediate', 'advanced'], weights=[0.6, 0.3, 0.1])[0]

def determine_body_goal(age: int, weight: int, height: int) -> str:
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        return 'gain muscle'
    elif bmi > 25:
        return 'lose weight'
    else:
        return random.choice(['gain muscle', 'increase strength'])

def determine_workout_days(age: int, fitness_level: str) -> int:
    if age > 60 or fitness_level == 'beginner':
        return random.randint(2, 4)
    elif age > 40 or fitness_level == 'intermediate':
        return random.randint(3, 5)
    else:
        return random.randint(4, 6)

def select_problem_areas(body_goal: str, age: int, fitness_level: str) -> List[str]:
    all_areas = ['weak_chest', 'weak_back', 'big_belly', 'small_arms', 'small_legs']
    if body_goal == 'lose weight':
        return random.sample(all_areas, k=min(3, random.randint(1, 4)))
    elif body_goal == 'gain muscle':
        muscle_areas = ['weak_chest', 'weak_back', 'small_arms', 'small_legs']
        return random.sample(muscle_areas, k=min(3, random.randint(1, 3)))
    else:  # increase strength
        if fitness_level == 'beginner' or age > 60:
            return random.sample(all_areas, k=min(2, random.randint(1, 2)))
        else:
            return random.sample(all_areas, k=min(3, random.randint(1, 3)))

def generate_workout_schedule(workout_days: int, problem_areas: List[str], fitness_level: str, body_goal: str) -> Dict[str, str]:
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    workout_types = ['leg day', 'back day', 'upper body', 'lower body', 'cardio', 'arm day', 'chest day', 'full body day']
    
    schedule = {day: 'rest' for day in days}

    # Prioritize problem areas
    for area in problem_areas:
        if area == 'weak_chest':
            workout_types.extend(['chest day'] * 2)
        elif area == 'weak_back':
            workout_types.extend(['back day'] * 2)
        elif area == 'big_belly':
            workout_types.extend(['cardio'] * 2)
        elif area == 'small_arms':
            workout_types.extend(['arm day'] * 2)
        elif area == 'small_legs':
            workout_types.extend(['leg day'] * 2)

    # Adjust based on fitness level and body goal
    if fitness_level == 'beginner':
        workout_types.extend(['full body day'] * 3)
    if body_goal == 'lose weight':
        workout_types.extend(['cardio'] * 2)
    elif body_goal == 'gain muscle':
        workout_types = [wt for wt in workout_types if wt != 'cardio'] + ['upper body', 'lower body'] * 2

    # Distribute workout days logically
    if workout_days <= 3:
        # For 1-3 workout days, ensure at least one rest day between workouts
        possible_start_days = days[:4]  # Monday to Thursday
        start_day = random.choice(possible_start_days)
        start_index = days.index(start_day)
        for i in range(workout_days):
            workout_index = (start_index + i * 2) % 7
            schedule[days[workout_index]] = random.choice(workout_types)
    elif workout_days <= 5:
        # For 4-5 workout days, try to have a rest day after every 2-3 workouts
        workout_indices = sorted(random.sample(range(7), workout_days))
        for i, index in enumerate(workout_indices):
            if i > 0 and index - workout_indices[i-1] == 1 and random.random() < 0.7:
                # 70% chance to swap with the next day if it's consecutive
                next_index = (index + 1) % 7
                if next_index not in workout_indices:
                    workout_indices[i] = next_index
        for index in workout_indices:
            schedule[days[index]] = random.choice(workout_types)
    else:
        # For 6-7 workout days, distribute randomly
        workout_days_list = random.sample(days, workout_days)
        for day in workout_days_list:
            schedule[day] = random.choice(workout_types)

    # Ensure no duplicate workout types in a week
    used_workouts = set()
    for day in days:
        if schedule[day] != 'rest':
            attempts = 0
            while schedule[day] in used_workouts and attempts < 10:
                schedule[day] = random.choice(workout_types)
                attempts += 1
            if attempts == 10:
                schedule[day] = 'full body day'  # Fallback to full body day if can't find unique workout
            used_workouts.add(schedule[day])

    return schedule

def save_to_csv(data: List[Dict], filename: str):
    headers = ['Gender', 'Age', 'BodyGoal', 'ProblemAreas', 'Height_cm', 'Weight_kg', 'FitnessLevel', 'WorkoutDaysPerWeek', 
               'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for entry in data:
            row = entry.copy()
            row['ProblemAreas'] = str(row['ProblemAreas']).replace("'", "")
            writer.writerow(row)

# Generate dummy data and save to CSV
dummy_data = generate_dummy_data(10000)  # Generate 100 entries
save_to_csv(dummy_data, 'dummy_data.csv')