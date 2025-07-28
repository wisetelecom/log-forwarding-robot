from enum import StrEnum


class LogLevel(StrEnum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Environment(StrEnum):
    LOCAL = 'LOCAL'
    TESTING = 'TESTING'
    PRODUCTION = 'PRODUCTION'

    @property
    def is_dev(self):
        """是否是开发环境"""
        return self in (self.LOCAL, self.TESTING)

    @property
    def is_testing(self):
        """是否是测试环境"""
        return self == self.TESTING

    @property
    def is_prod(self) -> bool:
        """是否是生产环境"""
        return self == self.PRODUCTION
