from core.database import db


# data1 = {
#     "id": 1,
#     "name": "The Musical Hop",
#     "genres": [
#         "Jazz",
#         "Reggae",
#         "Swing",
#         "Classical",
#         "Folk"
#     ],
#     "address": "1015 Folsom Street",
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "123-123-1234",
#     "website": "https://www.themusicalhop.com",
#     "facebook_link": "https://www.facebook.com/TheMusicalHop",
#     "seeking_talent": True,
#     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#     "past_shows": [
#         {
#             "artist_id": 4,
#             "artist_name": "Guns N Petals",
#             "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#             "start_time": "2019-05-21T21:30:00.000Z"
#         }

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # genres = db.Column(db.ARRAY(db.String()))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    # seeking_talent = db.Column(db.Boolean)
    # seeking_description = db.Column(db.String(500))
    # image_link = db.Column(db.String(500))
    # past_shows = db.Column(db.ARRAY(db.String()))
    # upcoming_shows = db.Column(db.String(500))
    # past_shows_count = db.Column(db.Integer)
    # upcoming_shows_count = db.Column(db.Integer)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate