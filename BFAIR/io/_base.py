__all__ = []

from cobra.core.singleton import Singleton


class _BaseFactory(metaclass=Singleton):
    def __init__(self, factory_method):
        self._factory_method = factory_method
        self._list = []

    def __dir__(self):
        return self._list

    def __getattr__(self, item):
        if item in self._list:
            return self._factory_method(item)
        return super().__getattribute__(item)

    def __getitem__(self, item):
        try:
            return self.__getattr__(item)
        except AttributeError:
            return None
