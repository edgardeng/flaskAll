class Config:

    SECRET_KEY = 'hard to guesss string'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    FLASK_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASK_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASK_MAIL_ADMIN = 'FLASKY_ADMIN'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_POSTS_PER_PAGE = 20
    FLASK_FOLLOWERS_PER_PAGE = 5
    FLASK_COMMENTS_PER_PAGE = 5
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:123456@localhost:3306/test'

    @staticmethod
    def init_app(app):
        pass

# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = ''
#
#
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = ''
#
#
# class ProductionConfig(Config):
#     PRODUCTION = True
#     SQLALCHEMY_DATABASE_URI = ''
#
#
# config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }

# config = Config()
