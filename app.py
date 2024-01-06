import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from core.database import db
from core.config import *

from models.artist import Artist
from models.venue import Venue
from models.show import Show

from flask_wtf import Form
from forms import *


app = Flask(__name__)
moment = Moment(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)

    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"

    return babel.dates.format_datetime(date, format, locale="en")

app.jinja_env.filters["datetime"] = format_datetime


@app.route("/")
def index():
    return render_template("pages/home.html")

@app.route("/venues")
def venues():
    all_venues = Venue.query.with_entities(
        # Venue.id,
        Venue.city,
        Venue.state
    ).group_by(
        Venue.city,
        Venue.state
    ).all()

    data = []

    for venue in all_venues:
        venue_data = {
            "city": venue.city,
            "state": venue.state,
            "venues": []
        }

        venues = Venue.query.filter_by(
            city=venue.city,
            state=venue.state
        ).all()

        for venue in venues:
            venue_data["venues"].append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(venue.shows)
            })

        data.append(venue_data)

    return render_template("pages/venues.html", areas=data);

@app.route("/venues/search", methods=["POST"])
def search_venues():
    search_term = request.form.get("search_term", "")
    venues = Venue.query.filter(Venue.name.ilike("%" + search_term + "%")).all()
    data = []

    for venue in venues:
        upcoming_shows = db.session.query(
            Show
        ).filter(
            Show.venue_id == venue.id,
            Show.start_time > datetime.now()
        ).all()

        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(upcoming_shows)
        })

    response = {
        "count": len(venues),
        "data": data
    }

    return render_template("pages/search_venues.html", results=response, search_term=request.form.get("search_term", ""))

@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    if not venue:
        return render_template("errors/404.html")
    
    upcoming_shows_query = db.session.query(
        Show
    ).join(
        Artist
    ).filter(
        Show.venue_id == venue_id
    ).filter(
        Show.start_time > datetime.now()
    ).all()

    past_shows_query = db.session.query(
        Show
    ).join(
        Artist
    ).filter(
        Show.venue_id == venue_id
    ).filter(
        Show.start_time < datetime.now()
    ).all()
    
    upcoming_shows = []
    past_shows = []

    for upcoming_show in upcoming_shows_query:
        upcoming_shows.append({
            "artist_id": upcoming_show.artist_id,
            "artist_name": upcoming_show.artist.name,
            "artist_image_link": upcoming_show.artist.image_link,
            "start_time": str(upcoming_show.start_time)
        })
    
    for past_show in past_shows_query:
        past_shows.append({
            "artist_id": past_show.artist_id,
            "artist_name": past_show.artist.name,
            "artist_image_link": past_show.artist.image_link,
            "start_time": str(past_show.start_time)
        })

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.replace("{", "").replace("}", "").split(","),
        "city": venue.city,
        "state": venue.state,
        "address": venue.address,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template("pages/show_venue.html", venue=data)

@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()

    return render_template("forms/new_venue.html", form=form)

@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    error = False
    form = VenueForm(request.form)

    try:
        venue = Venue(
            name = form.name.data,
            genres = form.genres.data,
            city = form.city.data,
            state = form.state.data,
            address = form.address.data,
            phone = form.phone.data,
            website = form.website_link.data,
            facebook_link = form.facebook_link.data,
            seeking_talent = True if form.seeking_talent.data else False,
            seeking_description = form.seeking_description.data,
            image_link = form.image_link.data
        )

        db.session.add(venue)
        db.session.commit()
    except:
        error = True

        db.session.rollback()

        flash("An error occurred. Venue " + request.form["name"] + " could not be listed.")
    
    finally:
        db.session.close()

        if not error:
            flash("Venue " + request.form["name"] + " was successfully listed!")

    return render_template("pages/home.html")

@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    error = False

    try:
        venue = Venue.query.get(venue_id)

        db.session.delete(venue)
        db.session.commit()
    except:
        error = True

        db.session.rollback()
    finally:
        db.session.close()

        if not error:
            flash("Venue " + venue.name + " was successfully deleted!")
        else:
            flash("An error occurred. Venue " + venue.name + " could not be deleted.")
    
    return render_template("pages/home.html")

@app.route("/artists")
def artists():
    all_artists = db.session.query(Artist).all()

    return render_template("pages/artists.html", artists=all_artists)

@app.route("/artists/search", methods=["POST"])
def search_artists():
    search_term = request.form.get("search_term", "")
    artists = Artist.query.filter(Artist.name.ilike("%" + search_term + "%")).all()
    data = []

    for artist in artists:
        upcoming_shows = db.session.query(
            Show
        ).filter(
            Show.artist_id == artist.id,
            Show.start_time > datetime.now()
        ).all()

        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(upcoming_shows)
        })

    response = {
        "count": len(artists),
        "data": data
    }

    return render_template("pages/search_artists.html", results=response, search_term=request.form.get("search_term", ""))

@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    artist_query = db.session.query(Artist).get(artist_id)

    if not artist_query:
        return render_template("errors/404.html")
    
    upcoming_shows_query = db.session.query(
        Show
    ).join(
        Artist
    ).filter(
        Show.artist_id == artist_id
    ).filter(
        Show.start_time > datetime.now()
    ).all()

    past_shows_query = db.session.query(
        Show
    ).join(
        Artist
    ).filter(
        Show.artist_id == artist_id
    ).filter(
        Show.start_time < datetime.now()
    ).all()

    upcoming_shows = []
    past_shows = []

    for upcoming_show in upcoming_shows_query:
        upcoming_shows.append({
            "venue_id": upcoming_show.venue_id,
            "venue_name": upcoming_show.venue.name,
            "artist_image_link": upcoming_show.artist.image_link,
            "start_time": str(upcoming_show.start_time)
        })
    
    for past_show in past_shows_query:
        past_shows.append({
            "venue_id": past_show.venue_id,
            "venue_name": past_show.venue.name,
            "artist_image_link": past_show.artist.image_link,
            "start_time": str(past_show.start_time)
        })

    data = {
        "id": artist_query.id,
        "name": artist_query.name,
        "genres": artist_query.genres.replace("{", "").replace("}", "").replace('"', "").split(","),
        "city": artist_query.city,
        "state": artist_query.state,
        "phone": artist_query.phone,
        "website": artist_query.website,
        "facebook_link": artist_query.facebook_link,
        "seeking_venue": artist_query.seeking_venue,
        "seeking_description": artist_query.seeking_description,
        "image_link": artist_query.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_artist.html", artist=data)

@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)

    if not artist:
        return render_template("errors/404.html")
    
    form = ArtistForm(
        name = artist.name,
        genres = artist.genres,
        city = artist.city,
        state = artist.state,
        phone = artist.phone,
        website_link = artist.website,
        facebook_link = artist.facebook_link,
        seeking_venue = artist.seeking_venue,
        seeking_description = artist.seeking_description,
        image_link = artist.image_link
    )

    return render_template("forms/edit_artist.html", form=form, artist=artist)

@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    error = False
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)

    try:
        artist.name = form.name.data
        artist.genres = form.genres.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = True if form.seeking_venue.data else False
        artist.seeking_description = form.seeking_description.data
        artist.image_link = form.image_link.data

        db.session.commit()
    except:
        error = True

        db.session.rollback()

        flash("An error occurred. Artist " + request.form["name"] + " could not be updated.")
    finally:
        db.session.close()

        if not error:
            flash("Artist " + request.form["name"] + " was successfully updated!")

    return redirect(url_for("show_artist", artist_id=artist_id))

@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    if not venue:
        return render_template("errors/404.html")
    
    form = VenueForm(
        name = venue.name,
        genres = venue.genres,
        city = venue.city,
        state = venue.state,
        address = venue.address,
        phone = venue.phone,
        website_link = venue.website,
        facebook_link = venue.facebook_link,
        seeking_talent = venue.seeking_talent,
        seeking_description = venue.seeking_description,
        image_link = venue.image_link
    )

    return render_template("forms/edit_venue.html", form=form, venue=venue)

@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    error = False
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)

    try:
        venue.name = form.name.data
        venue.genres = form.genres.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.website = form.website_link.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = True if form.seeking_talent.data else False
        venue.seeking_description = form.seeking_description.data
        venue.image_link = form.image_link.data

        db.session.commit()
    except:
        error = True

        db.session.rollback()

        flash("An error occurred. Venue " + request.form["name"] + " could not be updated.")
    finally:
        db.session.close()

        if not error:
            flash("Venue " + request.form["name"] + " was successfully updated!")

    return redirect(url_for("show_venue", venue_id=venue_id))

@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()

    return render_template("forms/new_artist.html", form=form)

@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    error = False
    form = ArtistForm(request.form)

    try:
        artist = Artist(
            name = form.name.data,
            genres = form.genres.data,
            city = form.city.data,
            state = form.state.data,
            phone = form.phone.data,
            website = form.website_link.data,
            facebook_link = form.facebook_link.data,
            seeking_venue = True if form.seeking_venue.data else False,
            seeking_description = form.seeking_description.data,
            image_link = form.image_link.data
        )

        db.session.add(artist)
        db.session.commit()
    except:
        error = True

        db.session.rollback()

        flash("An error occurred. Artist " + request.form["name"] + " could not be listed.")
    finally:
        db.session.close()

        if not error:
            flash("Artist " + request.form["name"] + " was successfully listed!")

    return render_template("pages/home.html")

@app.route("/shows")
def shows():
    all_shows = db.session.query(Show).join(Artist).join(Venue).all()
    data = []

    for show in all_shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })

    return render_template("pages/shows.html", shows=data)

@app.route("/shows/create")
def create_shows():
    form = ShowForm()

    return render_template("forms/new_show.html", form=form)

@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    error = False

    try:
        show = Show(
            artist_id = request.form["artist_id"],
            venue_id = request.form["venue_id"],
            start_time = request.form["start_time"]
        )

        db.session.add(show)
        db.session.commit()
    except:
        error = True

        db.session.rollback()

        flash("An error occurred. Show could not be listed.")
    finally:
        db.session.close()

        if not error:
            flash("Show was successfully listed!")

    return render_template("pages/home.html")

@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")


if __name__ == "__main__":
    app.run(
        host=APP_HOST,
        port=APP_PORT
    )
