from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Band(Base):
    __tablename__ = 'bands'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String, nullable=False)
    
    # Relationships
    concerts = relationship('Concert', back_populates='band')

    def concerts(self):
        return self.concerts

    def venues(self):
        return [concert.venue for concert in self.concerts]

    def play_in_venue(self, venue, date):
        concert = Concert(band_id=self.id, venue_id=venue.id, date=date)
        session.add(concert)
        session.commit()

    def all_introductions(self):
        return [f"Hello {concert.venue.city}!!!!! We are {self.name} and we're from {self.hometown}" for concert in self.concerts]

    @classmethod
    def most_performances(cls):
        # Assuming you have a session to query bands
        return session.query(Band).outerjoin(Band.concerts).group_by(Band.id).order_by(func.count(Concert.id).desc()).first()

class Venue(Base):
    __tablename__ = 'venues'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String, nullable=False)
    
    # Relationships
    concerts = relationship('Concert', back_populates='venue')
    
    def concerts(self):
        return self.concerts

    def bands(self):
        return [concert.band for concert in self.concerts]

    def concert_on(self, date):
        return session.query(Concert).filter_by(date=date, venue_id=self.id).first()

    def most_frequent_band(self):
        band_counts = {}
        for concert in self.concerts:
            band = concert.band
            if band not in band_counts:
                band_counts[band] = 0
            band_counts[band] += 1
        return max(band_counts, key=band_counts.get)

class Concert(Base):
    __tablename__ = 'concerts'
    
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey('bands.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)
    date = Column(String, nullable=False)
    
    # Relationships
    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')
    
    def band(self):
        return self.band

    def venue(self):
        return self.venue

    def hometown_show(self):
        return self.venue.city == self.band.hometown

    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
