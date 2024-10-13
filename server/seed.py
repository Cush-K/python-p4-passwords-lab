from models import db, User
from app import app
from faker import Faker
from config import bcrypt

fake=Faker()

with app.app_context():
    
    print("Clearing Database...")
    User.query.delete()
    
    raw_pass = fake.password(length=6, special_chars=True, digits=True, upper_case=True, lower_case=True)
    hash_pass = bcrypt.generate_password_hash(raw_pass).decode('utf-8')
    
    print("Seeding data...")
    users = []
    for _ in range(5):
        user = User(
            username = fake.name(),
            _password_hash = hash_pass
        )
        
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
    print("Complete!")