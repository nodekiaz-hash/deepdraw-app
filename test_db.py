from database import Session, User

session = Session()

users = session.query(User).all()

for u in users:
    print(u.email, u.credits)