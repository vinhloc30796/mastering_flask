from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func, text
from config import DevConfig
import datetime

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False,
                         index=True, unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='users',
        lazy='dynamic'
    )

    def __init__(self, username=""):
        self.username = username

    def __repr__(self):
        return f"<User {self.username}>"


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(), default=datetime.datetime.now)
    comments = db.relationship(
        'Comment',
        backref='posts',
        lazy='dynamic'
    )
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    tags = db.relationship(
        'Tag',
        secondary=post_tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title=""):
        self.title = title

    def __repr__(self):
        return f"<Post {self.title}>"


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title=""):
        self.title = title

    def __repr__(self):
        return f"<Tag {self.title}>"


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    def __repr__(self):
        return f"<Comment: {self.text[:15]}...>"


def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(post_tags.c.post_id).label('total')
    ).join(
        post_tags
    ).group_by(Tag).order_by(text('total DESC')).limit(5).all()

    return recent, top_tags


@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(
        page, app.config['POST_PER_PAGE'], False
    )
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)


@app.route('/posts_by_tag/<string:tag_name>')
def posts_by_tag(tag_name):
    pass


@app.route('/posts_by_user/<int:username>')
def posts_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
