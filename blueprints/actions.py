from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from datetime import date

from forms import AquariumActionsForm
from models import Aquarium, Action
from db import db

actions_views = Blueprint("actions", __name__, url_prefix="/aquariums/<string:aquarium_id>/actions")


@actions_views.route("/")
def index(aquarium_id):
    aquarium = Aquarium.query.filter_by(id=aquarium_id, user_id=current_user.id).first()
    if not aquarium:
        return redirect(url_for("aquariums.new"))

    return render_template("aquariums/actions_index.html", aquarium=aquarium, date=date)


@actions_views.route("/new/", methods=["GET", "POST"])
@login_required
def new(aquarium_id):
    form = AquariumActionsForm()
    aquarium = Aquarium.query.filter_by(id=aquarium_id, user_id=current_user.id).first()
    if not aquarium:
        return redirect(url_for("aquariums.new"))

    if form.validate_on_submit():
        action = Action(
            aquarium_id=aquarium.id,
            name=form.name.data,
            description=form.description.data,
            due_on=form.due_on.data
        )

        db.session.add(action)
        db.session.commit()
        return redirect(url_for("actions.index", aquarium_id=aquarium.id))
    return render_template("aquariums/actions_new.html", form=form, aquarium=aquarium)


@actions_views.route("/<string:action_id>/edit/", methods=["GET", "POST"])
@login_required
def edit(aquarium_id, action_id):
    action = Action.query.filter_by(id=action_id, aquarium_id=aquarium_id).first()
    if not action or action.aquarium.user_id != current_user.id:
        return redirect(url_for("actions.new", aquarium_id=aquarium_id))

    form = AquariumActionsForm(obj=action)
    if form.validate_on_submit():
        action.name = form.name.data
        action.description = form.description.data
        form.due_on = form.due_on.data

        db.session.add(action)
        db.session.commit()
        return redirect(url_for("actions.index", aquarium_id=action.aquarium.id))
    return render_template("aquariums/actions_edit.html", form=form, action=action)


@actions_views.route("/<string:action_id>/delete/", methods=["POST"])
@login_required
def delete(aquarium_id, action_id):
    action_query = Action.query.filter_by(id=action_id, aquarium_id=aquarium_id)
    action = action_query.first()
    if not action or action.aquarium.user_id != current_user.id:
        return redirect(url_for("actions.index", aquarium_id=aquarium_id))

    if action:
        aquarium = action.aquarium

        action_query.delete()
        db.session.commit()
        return redirect(url_for("actions.index", aquarium_id=aquarium.id))

    return redirect(url_for("aquariums.index"))
