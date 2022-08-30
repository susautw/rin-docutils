import functools

import pytest

from rin.docutils import markers


@pytest.fixture
def method_descriptor():
    @markers.decorator
    class method_descriptor:
        """Descriptor's doc"""

        def __init__(self, method):
            self._method = method
            self.__isabstractmethod__ = getattr(self._method, "__isabstractmethod__", False)

        def __get__(self, instance, owner):
            bm = self._method.__get__(instance, owner)

            @functools.wraps(self._method)
            def wrapper(*args, **kwargs):
                return bm(*args, **kwargs) + 1

            wrapper.__isabstractmethod__ = self.__isabstractmethod__
            return wrapper

    return method_descriptor
