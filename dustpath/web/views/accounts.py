from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from dustpath import models
from dustpath.web import forms
from dustpath.web import oauth2


module = Blueprint("accounts", __name__)


@module.route("/register", methods=("GET", "POST"))
def register():
    form = forms.RegisterForm()
    if not form.validate_on_submit():
        return render_template("/accounts/register.html", form=form)
    user = models.User.objects(username=form.username.data)
    if user:
        error_msg = "Username นี้ถูกใช้งานแล้ว"
        return render_template(
            "/accounts/register.html", form=form, error_msg=error_msg
        )
    user = models.User.objects(email=form.email.data)
    if user:
        error_msg = "Email นี้ถูกใช้งานแล้ว"
        return render_template(
            "/accounts/register.html", form=form, error_msg=error_msg
        )
    user = models.User()
    form.populate_obj(user)
    user.set_password(form.password.data)
    user.save()
    return redirect(url_for("accounts.login", messages="success"))


@module.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = forms.LoginForm()
    if not form.validate_on_submit():
        return render_template("/accounts/login.html", form=form)
    user = models.User.objects(username=form.username.data).first()
    if not user or not user.check_password(form.password.data):
        error_msg = "โปรดตรวจสอบ username และ password ของท่าน"
        # print(form.errors)
        return render_template("/accounts/login.html", form=form, error_msg=error_msg)
    if user.status == "disactive":
        error_msg = "โปรดติดต่อผู้ดูแลระบบเพื่อยืนยันบัญชีของท่าน"
        return render_template("/accounts/login.html", form=form, error_msg=error_msg)
    login_user(user)
    return redirect(url_for("dashboard.index", messages="success"))


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
    return redirect(url_for("site.index"))
