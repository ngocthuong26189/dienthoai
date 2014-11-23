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
from webapp.views.api import upload
from webapp.views.api import comment
from webapp.views.api import user as api_user
from webapp.views import image
from webapp.views.admin import dashboard
from webapp.views.admin import user
from webapp.views.admin import category
from webapp.views.admin import product
from webapp.views.admin import brand
from webapp.views.admin import order
from webapp.views.admin import sticky
from webapp.views.admin import news_category
from webapp.views.admin import question_category
from webapp.views.admin import news
from webapp.views.admin import question
from webapp.views.sites import product as sites_product
from webapp.views.sites import cart

# register blueprint to webapp
app.register_blueprint(home.module)
app.register_blueprint(upload.module, url_prefix="/api/v1/upload")
app.register_blueprint(api_user.module, url_prefix="/api/v1/user")
app.register_blueprint(comment.module, url_prefix="/api/v1/comment")
app.register_blueprint(image.module, url_prefix="/image")
app.register_blueprint(dashboard.module, url_prefix="/admin")
app.register_blueprint(user.module, url_prefix="/admin/user")
app.register_blueprint(category.module, url_prefix="/admin/category")
app.register_blueprint(product.module, url_prefix="/admin/product")
app.register_blueprint(brand.module, url_prefix="/admin/brand")
app.register_blueprint(order.module, url_prefix="/admin/order")
app.register_blueprint(sticky.module, url_prefix="/admin/sticky")
app.register_blueprint(news_category.module, url_prefix="/admin/news_category")
app.register_blueprint(question_category.module, url_prefix="/admin/question_category")
app.register_blueprint(news.module, url_prefix="/admin/news")
app.register_blueprint(question.module, url_prefix="/admin/question")
app.register_blueprint(sites_product.module, url_prefix="/product")
app.register_blueprint(cart.module, url_prefix="/cart")
