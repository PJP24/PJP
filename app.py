from flask import Flask, url_for, session, redirect
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'random secret key'
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='',
    client_secret='',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    issuer='https://accounts.google.com'
)


@app.route("/is-authenticated")
def is_authorized():
    return 'email' in session


@app.route("/")
def hello_world():
    email = dict(session).get("email", None)
    return f"<p>Hello, {email} - {is_authorized()}!</p>"


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    google.authorize_access_token()
    resp = google.get('userinfo')
    profile = resp.json()
    session['email'] = profile['email']
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)