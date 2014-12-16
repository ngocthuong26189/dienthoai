from flask import Blueprint
from flask import request, abort, redirect, session, make_response,url_for
from services import render, identity
from models.user import User
from models.category import Category
from flask_oauth import OAuth
import json, uuid
from urllib2 import Request, urlopen, URLError

module = Blueprint('home', __name__)

#Facebook login
FACEBOOK_APP_ID = '188477911223606'
FACEBOOK_APP_SECRET = '621413ddea2bcc5b2e83d42fc40495de'
oauth = OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)
@module.route('/facebook')
def facebook_index():
    return facebook.authorize(callback=url_for('.facebook_authorized',
        next=request.args.get('next') or None,
        _external=True))

@module.route('/login/facebook_authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return redirect(url_for('.login'))
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = identity.social_login(facebook_token=me.data.get("id"), google_token=None, username=me.data.get('name'),email = me.data.get('email'))
    if user:
        session['user'] = user.to_json()
        if request.args.get('next') is not None:
            return redirect(request.args.get('next'))
        return redirect(url_for('home.index'))
    else:
        return redirect(url_for('.login'))
    

# Khong duoc xoa ham nay
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
#End facebook login

#Google login
GOOGLE_CLIENT_ID = '1069800054786-128jio2h5p0fthm2bv14681s7bulqbhm.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'sXJJitRAz5Za4AMXnP6cm54a'
GOOGLE_REDIRECT_URI = '/google_authorized'  # one of the Redirect URIs from Google APIs console

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

# @module.route('/google')
# def google_index():
#     return redirect(url_for('.google_login',next=request.args.get('next') or request.referrer or None))


@module.route('/google')
def google_index():
    if request.args.get('next') is not None:
        session['google_next'] = request.args.get('next');
    callback=url_for('.google_authorized', _external=True)
    return google.authorize(callback=callback)



@module.route(GOOGLE_REDIRECT_URI)
@google.authorized_handler
def google_authorized(resp):
    if(resp is not None and resp['access_token'] is not None):
        access_token = resp['access_token']
        headers = {'Authorization': 'OAuth '+access_token}
        req = Request('https://www.googleapis.com/oauth2/v1/userinfo', None, headers)
        try:
            res = urlopen(req)
            data = json.loads(res.read())
            user = identity.social_login(facebook_token=None, google_token=data.get('id'), username=data.get('name'),email = data.get('email'))
            if user:
                session['user'] = user.to_json()
                if session.get('google_next') is not None:
                    google_next = session.get('google_next')
                    session['google_next'] = None
                    return redirect(google_next)
                return redirect(url_for('home.index'))
            else:
                return redirect(url_for('.login'))
        except URLError, e:
            return redirect(url_for('.login'))
        
    else: 
      return redirect(url_for('.login'))
@google.tokengetter
def get_access_token():
    return session.get('access_token')

#End google login

@module.route('/')
def index():
    # user = {}
    # if session.get('user') is not None:
    #     user = json.loads(session.get("user"))
    message = None
    index = Category.objects(name = 'index').first()
    if index is None:
        message = "You must create index category"
    return render.template('sites/home/index.html', category = index, message=message)    

@module.route('/<string:level_1>', methods = ['GET'])
def category_leve1(level_1):
    try:
        category = Category.objects(link=level_1).first()
        if category is None:
            return abort(404)
        if category.get_level() != 1:
            return abort(404)
        if category.parent.name == "index":
            pass
        return abort(404)
    except Exception, e:
        return abort(404)
 

@module.route('/X-4', methods = ['GET'])
def x4():
    return render.template('sites/dienthoai/x-4.html')


@module.route('/X-6', methods = ['GET'])
def x6():
    return render.template('sites/dienthoai/x-6.html')

@module.route('/X-8', methods = ['GET'])
def x8():
    return render.template('sites/dienthoai/x-8.html')


@module.route('/<string:level_1>/<string:level_2>', methods = ['GET'])
def category_leve2(level_1,level_2):
    try:
        vl1 = Category.objects(link=level_1).first()
        vl2 = Category.objects(link=level_2).first()
        return abort(404)  
    except Exception, e:
        return abort(404)

@module.route('/login', methods=['GET'])
def login():
    return render.template('sites/authen/login.html')

@module.route('/register', methods=['GET'])
def register():
    return render.template('sites/authen/register.html')

@module.route('/detail_temp', methods=['GET'])
def detail_temp():
    return render.template('sites/product/detail_new.html')

@module.route('/login', methods=['POST'])
def do_login():
    data = request.form.to_dict()
    username = data.get('username', None)
    password = data.get('password', None)
    if identity.authenticate(username, password):
        resp = make_response(redirect(request.args.get('next','/')))
        if json.loads(session['user']).get('permission', 1) > 2:
            userId = json.loads(session.get('user')).get('_id').get('$oid')
            sid = str(uuid.uuid4())
            user = User.objects(id=userId).get()
            user.sid = sid
            user.save()
            user.reload()
            session['user'] = user.to_json()
            resp.set_cookie('userId', userId)
            resp.set_cookie('sid',sid)
        return resp
    else:
        return render.template('sites/authen/login.html')

@module.route('/logout')
def logout():
    identity.logout()
    resp = make_response(redirect("/"))
    resp.set_cookie('sid', expires=0)
    resp.set_cookie('userId', expires=0)
    return resp
