from flask import Flask

import settings
from apps.apis.CE_apis import CE_bp


def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(settings.DevelopmentConfig)
    # register blueprint
    app.register_blueprint(CE_bp)

    return app