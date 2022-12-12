from flask import render_template,Blueprint, redirect, flash, jsonify, request
from flask_login import login_required, current_user
from devbus.utils.models import Post, User, DoesNotExist

main = Blueprint("main", "__name__")

@main.route("/")
def home():
    posts = Post.objects()
    return render_template("home.html",posts=posts)

@main.route("/user/<username>")
def view_user(username):
    try: 
        user = User.objects.get(username=username)
        posts = Post.objects(created_by=user.id) if user is not None else None
        return render_template("view_user.html", user=user, posts=posts)
    except DoesNotExist:
        flash("User you are looking for does not exist or has been deactivated", "red")
    return redirect("/")


@main.route("/search", methods=["GET", "POST"])
@login_required
def search_results():
    arg = request.form.get('search_field')
    filter = request.form.get('filter_select')
    match filter:
        case "username":
            users = User.objects(username__icontains=arg)
            posts = Post.objects(created_by__in=users)
        case "language":
            posts = Post.objects(code_language__icontains=arg)
        case _:
            posts = Post.objects()
    return render_template("search_results.html", posts=posts)


@main.route("/_search/<filter>/<arg>", methods=["GET", "POST"])
@login_required
def search(filter, arg=None):
    match filter:
        case "username":
            items = User.objects(username__icontains=arg)
        case "language":
            items = Post.objects(code_language__icontains=arg)
        case _:
            return jsonify(False)
    return jsonify(items=items)