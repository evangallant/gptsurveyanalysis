
class Config(object):
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    SECRET_KEY = "this-is-a-super-secret-key"

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}

## Enter your Open API Key here
OPENAI_API_KEY = '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'
