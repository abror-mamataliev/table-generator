class BaseConfig:
    """
    Base configuration
    """

    DEBUG = False
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    """
    Development configuration
    """

    DEBUG = True


class ProdConfig(BaseConfig):
    """
    Production configuration
    """

    pass
