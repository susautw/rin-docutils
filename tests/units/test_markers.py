import functools

from rin.docutils import markers


class TestMarkAsDecorator:

    def test_mark_a_function(self):
        @markers.decorator
        def function_decorator(fn):
            """Decorator's doc"""

            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs) + 1

            return wrapper

        @function_decorator
        def function(x: int) -> float:
            """Function's doc"""
            return x / 2

        assert function_decorator.__is_decorator__
        assert function_decorator.__doc__ == "Decorator's doc"
        assert function.__doc__ == "Function's doc"
        assert function.__annotations__ == {'x': int, 'return': float}
        assert function(4) == (4 / 2) + 1

    def test_mark_a_descriptor(self, method_descriptor):
        class Foo:
            """Class's doc"""

            @method_descriptor
            def method(self, x: int) -> float:
                """Method's doc"""
                return x / 2

        assert Foo.__doc__ == "Class's doc"
        assert method_descriptor.__doc__ == "Descriptor's doc"
        assert method_descriptor.__is_decorator__
        assert Foo.method.__doc__ == "Method's doc"
        assert Foo.method.__annotations__ == {'x': int, 'return': float}
        assert Foo().method(4) == (4 / 2) + 1
