from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transport_type = db.Column(db.String(10))
    from_city = db.Column(db.String(80), nullable=False)
    to_city = db.Column(db.String(80), nullable=False)
    departure = db.Column(db.String(50))
    seats_total = db.Column(db.Integer, default=40)
    seats_booked = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)

    def available_seats(self):
        return self.seats_total - self.seats_booked

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    passenger_name = db.Column(db.String(120))
    seats = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trip = db.relationship('Trip', backref='bookings')
