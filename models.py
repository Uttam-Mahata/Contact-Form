# models.py
from extensions import db #Import db from extension

class Contact(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), nullable=False)
     email = db.Column(db.String(120), nullable=False)
     subject = db.Column(db.String(200), nullable=False)
     message = db.Column(db.Text, nullable=False)

     def __repr__(self):
         return f'<Contact {self.name}>'