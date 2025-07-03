# seed_data.py
from database import SessionLocal, engine
from models import Base, Module, Lesson, SignEntry


def create_sample_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Create sample modules
        modules_data = [
            {
                "name": "Visual Communication Fundamentals",
                "description": "Foundation of visual attention and spatial awareness",
                "order_index": 1,
                "difficulty_level": 1,
                "estimated_duration": 180,
            },
            {
                "name": "Handshape and Movement Basics",
                "description": "Core handshapes and basic movements",
                "order_index": 2,
                "difficulty_level": 1,
                "estimated_duration": 240,
            },
            {
                "name": "Essential Vocabulary",
                "description": "Daily communication vocabulary",
                "order_index": 3,
                "difficulty_level": 2,
                "estimated_duration": 300,
            },
        ]

        for module_data in modules_data:
            module = Module(**module_data)
            db.add(module)

        db.commit()

        # Create sample lessons
        lessons_data = [
            {
                "module_id": 1,
                "title": "Understanding Visual Space",
                "description": "Learn about 3D signing space",
                "order_index": 1,
                "estimated_duration": 30,
                "content": {"type": "video", "url": "/videos/lesson1.mp4"},
            },
            {
                "module_id": 1,
                "title": "Facial Expression Recognition",
                "description": "Recognizing grammatical facial expressions",
                "order_index": 2,
                "estimated_duration": 45,
                "content": {
                    "type": "interactive",
                    "exercises": ["expression_matching"],
                },
            },
        ]

        for lesson_data in lessons_data:
            lesson = Lesson(**lesson_data)
            db.add(lesson)

        # Create sample sign entries
        signs_data = [
            {
                "word": "hello",
                "category": "greetings",
                "difficulty": 1,
                "description": "Basic greeting sign",
                "handshapes": {"dominant": "open_hand", "non_dominant": None},
                "movement_pattern": {"type": "wave", "direction": "right_to_left"},
                "location": "head_level",
                "palm_orientation": "forward",
            },
            {
                "word": "thank_you",
                "category": "courtesy",
                "difficulty": 1,
                "description": "Expression of gratitude",
                "handshapes": {"dominant": "flat_hand", "non_dominant": None},
                "movement_pattern": {"type": "forward", "direction": "away_from_body"},
                "location": "chin_level",
                "palm_orientation": "up",
            },
        ]

        for sign_data in signs_data:
            sign = SignEntry(**sign_data)
            db.add(sign)

        db.commit()

        print("Sample data created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
