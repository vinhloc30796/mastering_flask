class Config(object):
    pass


class ProdConfig(Config):
    SECRET_KEY = '\xb6\x03K\xca\xfe\x18&\x08c\xc3\xc8k]\x940\x80\x10\xfe{\x92\xd9\x84\x03\xf4'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    POST_PER_PAGE = 5
    SECRET_KEY = '\xa5E{b.\x8a\x8e\xee\xc8f\xc9\xb1#\xec$\x192\x14\xa4D\xf9\xa4"-'
