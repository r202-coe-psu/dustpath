from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from dustpath import models
from dustpath.web import forms
from dustpath.web import oauth2


module = Blueprint("accounts", __name__)

@module.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return render_template("/accounts/login.html")


@module.route("/login/<name>")
def login_oauth(name):
    client = oauth2.oauth2_client
    redirect_uri = url_for("accounts.authorized_oauth", name=name, _external=True)
    response = None
    if name == "google":
        response = client.google.authorize_redirect(redirect_uri)
    elif name == "facebook":
        response = client.facebook.authorize_redirect(redirect_uri)
    return response


@module.route("/auth/<name>")
def authorized_oauth(name):
    client = oauth2.oauth2_client
    remote = None
    try:

        if name == "google":
            remote = client.google
        elif name == "facebook":
            remote = client.facebook

        token = remote.authorize_access_token()

    except Exception as e:
        print(e)
        return redirect(url_for("accounts.login"))

    return oauth2.handle_authorized_oauth2(remote, token)


@module.route("/update_last_project_view")
@login_required
def update_last_project_view():
    project_id = request.args.get("project", default="")
    user = current_user._get_current_object()
    if project_id:
        project_selected = models.Project.objects(id=project_id).first()
        user.last_project_view = project_selected
        current_user.save()
    return redirect(url_for("dashboard.index"))


@module.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
