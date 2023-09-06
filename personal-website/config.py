import os


class Config:
    ROOT = os.getcwd()
    LOGS = os.path.join(ROOT, 'logs')




class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
}