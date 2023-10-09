from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class UserModel(db.Model):
    __tablename__ = 'UserModel'

    id = db.Column(db.Integer, primary_key=True)
    userMail = db.Column(db.String())
    username = db.Column(db.String(), unique = True)
    password = db.Column(db.String())
    jwt = db.Column(db.String())
    

    def __init__(self, userMail, username, password):
        self.userMail = userMail
        self.username = username
        self.password = password

    def serialize(self):
        return {"id": self.id,
                "email": self.userMail,
                "username": self.username,
                "password": self.password,
                "JWT": self.jwt
                }
