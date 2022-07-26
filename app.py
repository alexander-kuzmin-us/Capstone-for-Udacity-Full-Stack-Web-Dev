from os import environ as env
import json
from functools import wraps
from authlib.integrations.flask_client import OAuth
from flask import Flask, request
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from six.moves.urllib.parse import urlencode
from werkzeug.exceptions import HTTPException
from models import Charter, Skipper
from auth import requires_auth


import constants

AUTH0_CALLBACK_URL = constants.AUTH0_CALLBACK_URL
AUTH0_CLIENT_ID = constants.AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET = constants.AUTH0_CLIENT_SECRET
AUTH0_DOMAIN = constants.AUTH0_DOMAIN
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = constants.AUTH0_AUDIENCE

app = Flask(__name__, static_url_path='/public', static_folder='./public')

app.config['SQLALCHEMY_DATABASE_URI'] = env.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = constants.SECRET_KEY
app.debug = True

db = SQLAlchemy(app)

CORS(app, resources={r"/api/": {"origins": "*"}})


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


# Controllers API
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint

    res = auth0.authorize_access_token()
    token = res.get('access_token')

    # Store the user information in flask session.
    session['jwt_token'] = token

    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def requires_signed_in(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'jwt_token' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


@app.route('/dashboard')
@requires_signed_in
def dashboard():
    return render_template('dashboard.html',
                           token=session['jwt_token'],
                           )


@app.route('/charters')
@requires_auth('view:charters')
def get_charters(jwt):
    charters = Charter.query.all()
    charters = [charter.format() for charter in charters]
    for charter in charters:
        charter['skippers'] = [i.format() for i in charter['skippers']]
    return jsonify(charters)


@app.route('/skippers')
@requires_auth('view:skippers')
def get_skippers(jwt):
    skippers = Skipper.query.all()
    skippers = [skipper.format() for skipper in skippers]
    return jsonify(skippers)


@app.route('/charters/create', methods=['POST'])
@requires_auth('create:charter')
def post_new_charter(jwt):
    body = request.get_json()

    charters_name = body.get('charters_name', None)
    departure_date = body.get('departure_date', None)

    charter = Charter(charters_name=charters_name, departure_date=departure_date)
    charter.insert()
    new_charter = Charter.query.get(charter.id)
    new_charter = new_charter.format()

    return jsonify({
        'success': True,
        'created': charter.id,
        'new_charter': new_charter
    })


@app.route('/skippers/create', methods=['POST'])
@requires_auth('create:skipper')
def post_new_skipper(jwt):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    charter_id = body.get('charter_id', None)

    skipper = Skipper(name=name, age=age, gender=gender, charter_id=charter_id)
    skipper.insert()
    new_skipper = Skipper.query.get(skipper.id)
    new_skipper = new_skipper.format()

    return jsonify({
        'success': True,
        'created': skipper.id,
        'new_skipper': new_skipper
    })


@app.route('/charters/delete/<int:charter_id>', methods=['DELETE'])
@requires_auth('delete:charter')
def delete_charter(jwt, charter_id):
    Charter.query.filter(Charter.id == charter_id).delete()
    db.session.commit()
    db.session.close()
    return jsonify({
        'success': True,
        'message': 'Deleted'
    })


@app.route('/skippers/delete/<int:skipper_id>', methods=['DELETE'])
@requires_auth('delete:skipper')
def delete_skipper(jwt, skipper_id):
    Skipper.query.filter(Skipper.id == skipper_id).delete()
    db.session.commit()
    db.session.close()
    return jsonify({
        'success': True,
        'message': 'Deleted'
    })


@app.route('/skippers/patch/<int:skipper_id>', methods=['PATCH'])
@requires_auth('edit:skipper')
def patch_skipper(jwt, skipper_id):
    skipper = Skipper.query.filter(Skipper.id == skipper_id)
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    charter_id = body.get('charter_id', None)
    skipper.name = name
    skipper.age = age
    skipper.gender = gender
    skipper.charter_id = charter_id
    skipper.update()
    return jsonify({
        'success': True,
        'message': 'Updated'
    })


@app.route('/charters/patch/<int:charter_id>')
@requires_auth('edit:charter')
def patch_charter(jwt, charter_id):
    charter = Charter.query.filter(Charter.id == charter_id)
    body = request.get_json()
    charters_name = body.get('charters_name', None)
    departure_date = body.get('departure_date', None)
    charter.charters_name = charters_name
    charter.departure_date = departure_date
    charter.update()
    return jsonify({
        'success': True,
        'message': 'Updated'
    })


if __name__ == "__main__":
    app.run()
