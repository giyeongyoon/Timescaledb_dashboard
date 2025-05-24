# dashboard/app.py
from flask import Flask, redirect, url_for, make_response, jsonify, request
from flask_login import LoginManager, current_user
from dash_apps.latest_app import init_latest_dash
from dash_apps.graph_app import init_graph_dash
from database.postgresql import get_conn_db
from auth.login import auth
from auth.user import User
from common.config import conf

conn = get_conn_db()

app = Flask(__name__, static_url_path='/static')
app.secret_key = conf.get("secret_key")

app.register_blueprint(auth, url_prefix='/auth')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(useremail):
    if useremail == conf.get("email"):
        return User(useremail)

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

@app.before_request
def restrict_routes():
    allowed_paths = ["/auth", "/auth/login", "/static"]
    if (not current_user.is_authenticated
        and not any(request.path.startswith(p) for p in allowed_paths)):
        return redirect(url_for("auth.login"))


init_latest_dash(app, conn)
init_graph_dash(app, conn)


if __name__ == "__main__":
    app.run(debug=True)