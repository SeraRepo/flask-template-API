from flask import Flask, Response
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate

from config import *
from models.models import db
from routes.user import user_bp
from routes.auth import auth_bp

def create_db():
    """
    Create the database for the project
    """
    db.create_all()
    db.session.commit()

def create_app():
    """
    Initialize the application: create the Flaks app, create the database

    Returns:
        Flaks application: Our Flask application
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    create_db()
    migrate = Migrate(app, db)
    CORS(app)
    
    return app

app = create_app()

app.register_blueprint(user_bp, url_prefix=URL_PREFIX)
app.register_blueprint(auth_bp, url_prefix=URL_PREFIX)

@app.route('/ping', methods=['GET'])
@cross_origin()
def ping():
    """
    Ping route to test if the API is working

    Returns:
        text: "pong" text
    """
    return Response("pong", mimetype='text/html')

if __name__ == "__main__":
    print("API start")
    try:
        app.run(host="0.0.0.0", port=8000, debug=True)
    except Exception as e:
        print(str(e))
        pass