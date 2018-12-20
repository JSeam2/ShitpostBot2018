class BaseConfig:
    """
    Base Config
    """
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """
    Development Config
    """
    pass

class TestingConfig(BaseConfig):
    """
    Testing Config
    """
    TESTING = True


class ProductionConfig(BaseConfig):
    """
    Production Config
    """
    pass