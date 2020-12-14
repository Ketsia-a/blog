import os

class Config:
  
    SECRET_KEY = 'reality321'
    QUOTES_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://kets:ketsia321@localhost/blog"
    UPLOADED_PHOTOS_DEST ='app/static/photos'
  
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
   


class ProdConfig(Config):
    pass

  


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}