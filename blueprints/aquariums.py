from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

from forms import AquariumForm
from models import Aquarium
from db import db

aquariums_views = Blueprint("aquariums", __name__, url_prefix="/aquariums")


@aquariums_views.route("/")
@login_required
def index():
    aquariums = Aquarium.query.filter_by(user_id=current_user.id)
    return render_template("aquariums/aquariums_index.html", aquariums=aquariums)


@aquariums_views.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = AquariumForm()
    if form.validate_on_submit():
        aquarium = Aquarium(
            user_id=current_user.id,
            name=form.name.data
        )
        db.session.add(aquarium)
        db.session.commit()
        return redirect(url_for("aquariums.index"))

    return render_template("aquariums/aquariums_new_form.html", form=form)


@aquariums_views.route("/<string:aquarium_id>/edit", methods=["GET", "POST"])
@login_required
def edit(aquarium_id):
    aquarium = Aquarium.query.filter_by(id=aquarium_id, user_id=current_user.id).first()
    if not aquarium:
        return redirect(url_for("aquariums.new"))

    form = AquariumForm(obj=aquarium)
    if form.validate_on_submit():
        aquarium.name = form.name.data

        db.session.add(aquarium)
        db.session.commit()
        return redirect(url_for("aquariums.index"))

    return render_template("aquariums/aquariums_edit_form.html", form=form, aquarium=aquarium)


@aquariums_views.route("/<string:aquarium_id>/delete", methods=["POST"])
@login_required
def delete(aquarium_id):
    aquarium = Aquarium.query.filter_by(id=aquarium_id, user_id=current_user.id)
    if aquarium:
        aquarium.delete()
        db.session.commit()

    return redirect(url_for("aquariums.index"))
