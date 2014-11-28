from flask import Flask, g, session
from services import system
from services import render
from services import identity
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = 'deotraloithetgaovoich'

@app.before_request
def hook_request():
    system.connect_mongo()
    g.user = identity.current_user()


# Some error handler
@app.errorhandler(404)
def not_found(err):
    return render.template('raises/404.html', error=err), 404

@app.errorhandler(500)
def not_found(err):
    return "Oops, 500, Server error", 500

@app.errorhandler(400)
def not_found(err):
    return render.template('raises/400.html', error=err), 400

@app.errorhandler(403)
def not_found(err):
    return "Oops, 403, Forbidden", 403

@app.template_filter('ng')
def angular(s):
    return '{{ ' + str(s) + ' }}'

# import webapp modules
from webapp.views import home
from webapp.views import image
from webapp.views.admin import dashboard


# register blueprint to webapp
app.register_blueprint(home.module)
app.register_blueprint(image.module, url_prefix="/image")
app.register_blueprint(dashboard.module, url_prefix="/admin")

