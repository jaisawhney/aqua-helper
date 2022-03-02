from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from forms import AquariumLivestockForm
from models import Aquarium, Livestock
from db import db

livestock_views = Blueprint("livestock", __name__, url_prefix="/aquariums/<string:aquarium_id>/livestock/")


@livestock_views.route("/")
@login_required
def index(aquarium_id):
    aquarium = Aquarium.query.filter_by(id=aquarium_id, user_id=current_user.id).first()
    if not aquarium:
        return redirect(url_for("aquariums.new"))
    return render_template("aquariums/livestock_index.html", aquarium=aquarium)


@livestock_views.route("/new/", methods=["GET", "POST"])
@login_required
def new(aquarium_id):
    form = AquariumLivestockForm()
    aquarium = Aquarium.query.filter_by(id=aquarium_id, user_id=current_user.id).first()
    if not aquarium:
        return redirect(url_for("aquariums.new"))
    if form.validate_on_submit():
        livestock = Livestock(
            aquarium_id=aquarium.id,
            name=form.name.data,
            quantity=form.quantity.data,
            added_on=form.added_on.data
        )
        db.session.add(livestock)
        db.session.commit()
        return redirect(url_for("livestock.index", aquarium_id=aquarium.id))
    return render_template("aquariums/livestock_new.html", form=form, aquarium=aquarium)


@livestock_views.route("/<string:livestock_id>/delete/", methods=["POST"])
@login_required
def delete(aquarium_id, livestock_id):
    livestock_query = Livestock.query.filter_by(id=livestock_id, aquarium_id=aquarium_id)
    livestock = livestock_query.first()
    if not livestock or livestock.aquarium.user_id != current_user.id:
        return redirect(url_for("actions.index", aquarium_id=aquarium_id))

    if livestock:
        aquarium = livestock.aquarium
        livestock_query.delete(synchronize_session="fetch")
        db.session.commit()
        return redirect(url_for("livestock.index", aquarium_id=aquarium.id))

    # Entry doesn't exist
    return redirect(url_for("aquariums.index"))
