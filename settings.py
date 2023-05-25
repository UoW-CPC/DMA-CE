class Config:
    SECRET_KEY = 'afsjskahsfdkhadsjk'

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False