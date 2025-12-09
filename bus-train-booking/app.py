from flask import Flask, render_template, request, jsonify
from models import db, Trip, Booking
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create DB tables on startup
with app.app_context():
    db.create_all()

    # Insert sample trips if empty
    if Trip.query.count() == 0:
        sample = [
            Trip(transport_type='bus', from_city='Delhi', to_city='Agra', departure='09:00 AM', seats_total=40, price=300),
            Trip(transport_type='train', from_city='Delhi', to_city='Agra', departure='06:00 PM', seats_total=200, price=150),
        ]
        db.session.bulk_save_objects(sample)
        db.session.commit()


@app.route('/')
def index():
    trips = Trip.query.all()
    return render_template('index.html', trips=trips)


@app.route('/bookings')
def view_bookings():
    bookings = Booking.query.all()
    return render_template('bookings.html', bookings=bookings)


@app.route('/api/trips')
def api_trips():
    trips = Trip.query.all()
    data = [
        {
            'id': t.id,
            'transport_type': t.transport_type,
            'from_city': t.from_city,
            'to_city': t.to_city,
            'departure': t.departure,
            'price': t.price,
            'available_seats': t.available_seats()
        }
        for t in trips
    ]
    return jsonify(data)


@app.route('/api/book', methods=['POST'])
def api_book():
    payload = request.get_json()
    trip_id = payload.get('trip_id')
    name = payload.get('passenger_name')
    seats = int(payload.get('seats', 1))

    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    if seats > trip.available_seats():
        return jsonify({'error': 'Not enough seats'}), 400

    booking = Booking(trip_id=trip_id, passenger_name=name, seats=seats)
    trip.seats_booked += seats

    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': 'Booking successful', 'booking_id': booking.id})


if __name__ == "__main__":
    app.run(debug=True)
