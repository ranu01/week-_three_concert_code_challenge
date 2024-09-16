from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///concerts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Band(db.Model):
    __tablename__ = 'bands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hometown = db.Column(db.String, nullable=False)
    
    # Relationships
    concerts = db.relationship('Concert', back_populates='band')

    def concerts(self):
        return self.concerts

    def venues(self):
        return [concert.venue for concert in self.concerts]

    def play_in_venue(self, venue, date):
        concert = Concert(band_id=self.id, venue_id=venue.id, date=date)
        db.session.add(concert)
        db.session.commit()

    def all_introductions(self):
        return [f"Hello {concert.venue.city}!!!!! We are {self.name} and we're from {self.hometown}" for concert in self.concerts]

    @classmethod
    def most_performances(cls):
        return db.session.query(Band).outerjoin(Band.concerts).group_by(Band.id).order_by(db.func.count(Concert.id).desc()).first()

class Venue(db.Model):
    __tablename__ = 'venues'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    
    # Relationships
    concerts = db.relationship('Concert', back_populates='venue')
    
    def concerts(self):
        return self.concerts

    def bands(self):
        return [concert.band for concert in self.concerts]

    def concert_on(self, date):
        return db.session.query(Concert).filter_by(date=date, venue_id=self.id).first()

    def most_frequent_band(self):
        band_counts = {}
        for concert in self.concerts:
            band = concert.band
            if band not in band_counts:
                band_counts[band] = 0
            band_counts[band] += 1
        return max(band_counts, key=band_counts.get)

class Concert(db.Model):
    __tablename__ = 'concerts'
    
    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('bands.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    date = db.Column(db.String, nullable=False)
    
    # Relationships
    band = db.relationship('Band', back_populates='concerts')
    venue = db.relationship('Venue', back_populates='concerts')
    
    def band(self):
        return self.band

    def venue(self):
        return self.venue

    def hometown_show(self):
        return self.venue.city == self.band.hometown

    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"

@app.route('/bands', methods=['GET'])
def get_bands():
    bands = Band.query.all()
    return jsonify([{'id': band.id, 'name': band.name, 'hometown': band.hometown} for band in bands])

@app.route('/venues', methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    return jsonify([{'id': venue.id, 'title': venue.title, 'city': venue.city} for venue in venues])

@app.route('/concerts', methods=['GET'])
def get_concerts():
    concerts = Concert.query.all()
    return jsonify([{'id': concert.id, 'band_id': concert.band_id, 'venue_id': concert.venue_id, 'date': concert.date} for concert in concerts])

@app.route('/band/<int:band_id>/play', methods=['POST'])
def band_play_in_venue(band_id):
    data = request.json
    band = Band.query.get_or_404(band_id)
    venue = Venue.query.get_or_404(data['venue_id'])
    date = data['date']
    try:
        band.play_in_venue(venue, date)
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Error scheduling concert'}), 400
    return jsonify({'message': 'Concert scheduled successfully'})

@app.route('/band/<int:band_id>/introductions', methods=['GET'])
def get_band_introductions(band_id):
    band = Band.query.get_or_404(band_id)
    introductions = band.all_introductions()
    return jsonify({'introductions': introductions})

@app.route('/venue/<int:venue_id>/most_frequent_band', methods=['GET'])
def get_most_frequent_band(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    band = venue.most_frequent_band()
    if band:
        return jsonify({'id': band.id, 'name': band.name, 'hometown': band.hometown})
    return jsonify({'error': 'No bands found'}), 404

@app.route('/bands/most_performances', methods=['GET'])
def get_band_most_performances():
    band = Band.most_performances()
    if band:
        return jsonify({'id': band.id, 'name': band.name, 'hometown': band.hometown})
    return jsonify({'error': 'No bands found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
