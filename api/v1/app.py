from flask import Flask
from models import storage
import os
from api.v1.views import app_views
app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_request
def call_storage_close():
    storage.close()


if __name__ == "__main__":
    hosts = os.getenv('HBNB_API_HOST', '0.0.0.0')
    ports = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=hosts, port=int(ports), threaded=True)


