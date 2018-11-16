class Config(object):
    """Base config class."""
    pass

class ProdConfig(Config):
    """Production config class."""
    DEBUG = False

    # Session key
    SECURE_KEY = 'jiami'

    # MySQL connection  mysql://username:password@server/db
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jzdcadm:Jzdc@192.168.3.135:3306/Jzdcprd_test2'

class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True

    # Session key
    SECURE_KEY = '123456'
    TOKEN_LIFETIME = 60*60*24

    # MySQL connection  mysql://username:password@server/db
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jzdcadm:Jzdc@2018@192.168.3.135:3306/Jzdcprd_test2?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

