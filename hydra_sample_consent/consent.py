from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask.ext.login import LoginManager, login_required, login_user, logout_user
import requests
from hydra.consent import Consent

app = Flask(__name__, template_folder="template")
app.secret_key = 'idp secret key'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


def auth(name, password):
    # IDPの認証用APIを叩く(全くセキュアでないサンプルAPI)
    r = requests.get('http://localhost:65001/api/auth',
                     params=dict(username=name, password=password,))
    if r:
        return User(name)
    else:
        return None


class User():
    def __init__(self, username, data=None):
        self.username = username
        self.data = data

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @classmethod
    def auth(cls, username, password):
        if auth(username, password):
            return User(username)
        return None


@login_manager.user_loader
def load_user(username):
    return User(username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session['next'] = request.args.get('next', '/')
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.auth(username, password)
        if user:
            print("login!!!!!!!!!!!!")
            login_user(user)
            return redirect(session['next'])
        else:
            error = "ユーザID またはパスワードが違います"
            return render_template("login.html", username=username, password=password, error=error)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# サンプルのため雑なスコープ
cons = Consent('http://localhost:4444', 'consent-app', 'consent-secret')


@app.route("/consent", methods=["GET", "POST"])
@login_required
def consent():
    if request.method == 'GET':
        challenge = request.args.get('challenge')
        claims = cons.get_claims(challenge)
        return render_template("consent.html", client_id=claims['aud'], scopes=claims['scp'])
    else:
        agree = request.form.get('action') != 'disagree'
        if agree:
            return redirect(cons.get_success_response())
        else:
            return redirect(cons.get_deny_response())


def cli():
    app.run(host="0.0.0.0", port=65003)


if __name__ == "__main__":
    cli()
