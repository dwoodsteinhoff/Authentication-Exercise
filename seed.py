from models import User, db, Feedback
from app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Feedback.query.delete()

# Add users
joe_smith = User(username='bigman1', 
                 password=f'{bcrypt.generate_password_hash("bigman1").decode("utf8")}', 
                 email='bigman1@gmail.com',
                 first_name='Joe', 
                 last_name='Smith')

jane_smooth = User(username='biggal1', 
                   password=f'{bcrypt.generate_password_hash("biggal1").decode("utf8")}', 
                   email='biggal1@gmail.com',
                   first_name='Jane', 
                   last_name='Smooth')

feedback1 = Feedback(title = 'First Feedback!',
                    content = 'You Do Good Work',
                    username = 'biggal1')

feedback2 = Feedback(title = 'Yet Another Feedback!',
                    content = 'You need to work 40 hours',
                    username = 'bigman1')

# Add new objects to session, so they'll persist
db.session.add(joe_smith)
db.session.add(jane_smooth)
db.session.add(feedback1)
db.session.add(feedback2)

# Commit--otherwise, this never gets saved!
db.session.commit()
