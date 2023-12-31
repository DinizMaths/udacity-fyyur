from core.database import db


# data1={
#     "id": 4,
#     "name": "Guns N Petals",
#     "genres": ["Rock n Roll"],
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "326-123-5000",
#     "website": "https://www.gunsnpetalsband.com",
#     "facebook_link": "https://www.facebook.com/GunsNPetals",
#     "seeking_venue": True,
#     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     "past_shows": [
#         {
#             "venue_id": 1,
#             "venue_name": "The Musical Hop",
#             "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#             "start_time": "2019-05-21T21:30:00.000Z"
#         }
#     ],
#     "upcoming_shows": [],
#     "past_shows_count": 1,
#     "upcoming_shows_count": 0,
# }

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    # past_shows = db.Column(db.ARRAY(db.String()))
    # upcoming_shows = db.Column(db.String(500))
    # past_shows_count = db.Column(db.Integer)
    # upcoming_shows_count = db.Column(db.Integer)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate