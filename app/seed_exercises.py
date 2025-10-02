from app.db import SessionLocal
from app.models.exercise import Exercise

def seed_exercises():
    db = SessionLocal()

    exercises = [
        Exercise(
            name="Push-Up",
            description="A bodyweight exercise that strengthens the chest, shoulders, and triceps.",
            instructions="Keep body straight, lower chest to floor, push back up.",
            target_muscles="Chest, Shoulders, Triceps",
            equipment="None",
            difficulty="Beginner"
        ),
        Exercise(
            name="Pull-Up",
            description="Upper-body strength exercise performed by pulling up body weight.",
            instructions="Hang from a bar with palms facing away, pull body up until chin passes bar, lower back down.",
            target_muscles="Back, Biceps, Shoulders",
            equipment="Pull-up Bar",
            difficulty="Intermediate"
        ),
        Exercise(
            name="Squat",
            description="A lower body exercise targeting quadriceps, glutes, and hamstrings.",
            instructions="Stand with feet shoulder-width apart, bend knees and hips to lower body, return to standing.",
            target_muscles="Quadriceps, Glutes, Hamstrings",
            equipment="None",
            difficulty="Beginner"
        ),
        Exercise(
            name="Deadlift",
            description="A compound lift that builds strength in the posterior chain.",
            instructions="Stand with feet under barbell, grip bar, keep back straight, and lift to standing.",
            target_muscles="Back, Glutes, Hamstrings",
            equipment="Barbell",
            difficulty="Intermediate"
        ),
        Exercise(
            name="Bench Press",
            description="A compound lift targeting the chest, shoulders, and triceps.",
            instructions="Lie on bench, lower barbell to chest, press it back up until arms are straight.",
            target_muscles="Chest, Shoulders, Triceps",
            equipment="Barbell, Bench",
            difficulty="Intermediate"
        ),
        Exercise(
            name="Overhead Press",
            description="A shoulder press performed standing or seated.",
            instructions="Press barbell or dumbbells overhead until arms are straight, lower under control.",
            target_muscles="Shoulders, Triceps, Upper Chest",
            equipment="Barbell or Dumbbells",
            difficulty="Intermediate"
        ),
        Exercise(
            name="Bicep Curl",
            description="Isolation movement for the biceps.",
            instructions="Hold dumbbells at sides, curl weights toward shoulders, lower slowly.",
            target_muscles="Biceps",
            equipment="Dumbbells or Barbell",
            difficulty="Beginner"
        ),
        Exercise(
            name="Tricep Dip",
            description="Bodyweight exercise for triceps and chest.",
            instructions="Support body on parallel bars, lower until elbows bent at 90 degrees, push back up.",
            target_muscles="Triceps, Chest, Shoulders",
            equipment="Dip Bars",
            difficulty="Intermediate"
        ),
        Exercise(
            name="Lunge",
            description="A unilateral lower body exercise.",
            instructions="Step forward with one leg, lower until both knees are bent at 90 degrees, push back up.",
            target_muscles="Quadriceps, Glutes, Hamstrings",
            equipment="None",
            difficulty="Beginner"
        ),
        Exercise(
            name="Plank",
            description="Core stability exercise.",
            instructions="Hold body in straight line supported by forearms and toes, engage core.",
            target_muscles="Core, Shoulders",
            equipment="None",
            difficulty="Beginner"
        ),
        Exercise(
            name="Mountain Climbers",
            description="Cardio and core exercise performed in plank position.",
            instructions="Start in push-up position, drive knees alternately toward chest at fast pace.",
            target_muscles="Core, Shoulders, Legs",
            equipment="None",
            difficulty="Beginner"
        ),
        Exercise(
            name="Burpee",
            description="Full-body conditioning exercise.",
            instructions="From standing, drop into push-up, jump feet back in, and explosively jump upward.",
            target_muscles="Full Body, Core, Legs",
            equipment="None",
            difficulty="Intermediate"
        ),
        Exercise(
            name="Crunch",
            description="Abdominal isolation exercise.",
            instructions="Lie on back with knees bent, lift shoulders off ground by contracting abs.",
            target_muscles="Abdominals",
            equipment="None",
            difficulty="Beginner"
        ),
        Exercise(
            name="Russian Twist",
            description="Rotational core exercise.",
            instructions="Sit on floor with knees bent, lean back slightly, twist torso side to side.",
            target_muscles="Obliques, Core",
            equipment="Medicine Ball (optional)",
            difficulty="Beginner"
        ),
        Exercise(
            name="Leg Raise",
            description="Lower abdominal exercise.",
            instructions="Lie on back, lift legs together until vertical, lower slowly without touching ground.",
            target_muscles="Lower Abdominals, Hip Flexors",
            equipment="None",
            difficulty="Intermediate"
        ),
        Exercise(
            name="Calf Raise",
            description="Isolation exercise for calves.",
            instructions="Stand upright, raise heels off floor, pause, lower slowly.",
            target_muscles="Calves",
            equipment="None or Barbell",
            difficulty="Beginner"
        ),
        Exercise(
            name="Row",
            description="Pulling exercise for back muscles.",
            instructions="Bend forward with flat back, pull barbell or dumbbells toward torso, lower slowly.",
            target_muscles="Back, Biceps, Rear Shoulders",
            equipment="Barbell or Dumbbells",
            difficulty="Intermediate"
        ),
        Exercise(
            name="Shoulder Lateral Raise",
            description="Isolation exercise for shoulders.",
            instructions="Hold dumbbells at sides, lift arms out to shoulder height, lower slowly.",
            target_muscles="Lateral Deltoids",
            equipment="Dumbbells",
            difficulty="Beginner"
        ),
        Exercise(
            name="Bicycle Crunch",
            description="Dynamic core exercise.",
            instructions="Lie on back, bring opposite elbow to opposite knee in pedaling motion.",
            target_muscles="Abdominals, Obliques",
            equipment="None",
            difficulty="Beginner"
        ),
        Exercise(
            name="Farmer’s Carry",
            description="Grip and core stability exercise.",
            instructions="Hold heavy dumbbells at sides, walk for distance while maintaining upright posture.",
            target_muscles="Forearms, Grip, Core, Legs",
            equipment="Dumbbells or Kettlebells",
            difficulty="Intermediate"
        ),
    ]

    for ex in exercises:
        exists = db.query(Exercise).filter_by(name=ex.name).first()
        if not exists:
            db.add(ex)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_exercises()
    print("✅ 20 exercises seeded successfully.")
