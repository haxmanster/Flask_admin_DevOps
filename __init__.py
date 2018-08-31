from flask import Flask, url_for
from flask_admin import Admin, BaseView, expose
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
import os


app = Flask(__name__)


app.config['SECRET_KEY'] = os.urandom(24)

# Create in-memory database
app.config['DATABASE_FILE'] = 'static/db/sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create user model.


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class Start(BaseView):
    @expose('/')
    def index(self):
        url = url_for('.test')
        return self.render('index.html', url=url)

    @expose('/test/')
    def test(self):
        url = url_for('testadmin.index')
        return self.render('index.html', url=url)

class Login(BaseView):
    @expose('/')
    def index(self):
        url = url_for('.test')
        return self.render('test.html', url=url)

    @expose('/test/')
    def test(self):
        url = url_for('testuser.index')
        return self.render('test.html', url=url)




admin = Admin(app,  name='DevOps', template_mode='bootstrap3')
path = op.join(op.dirname(__file__), 'storage')
admin.add_view(Start(endpoint='testadmin'))
admin.add_view(Login(endpoint='testuser'))
admin.add_view(FileAdmin(path, '/storage/', name='Pliki'))

app.run(port=5105)
