class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    database_name = "trivia"
    database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
    SQLALCHEMY_DATABASE_URI = database_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    database_name = "trivia_test"
    database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
    SQLALCHEMY_DATABASE_URI = database_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
