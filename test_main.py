from main import trace
from foo import example_function, Foo, function_returning_dict, returns_a_class


# helper fun
def traverse_dict(d, target, path=None):
    for k, v in d.items():
        full_key = f"{path}|{k}" if path else k
        if k == target:
            return full_key
        if isinstance(v, dict):
            return traverse_dict(v, target, full_key)
    return None


def test_example_function():
    with trace() as actual:
        f = Foo()
        example_function(1, 2, f)
    for k in actual:
        if 'init' in k:
            assert actual[k]["args"] == {"bar": [None]}
            assert actual[k]["return"] == [None]
        elif 'example_function' in k:
            assert actual[k]["args"] == {"a": [1], "b": [2], "foo": ["USER_CLASS|foo::Foo"]}
            assert actual[k]["return"] == [3]


def test_if_global_context_is_not_polluted_by_previous_test_invocation():
    with trace() as actual:
        f = Foo()
        example_function(1, 2, f)
        example_function(3, 4, None)
    for k in actual:
        if 'init' in k:
            assert actual[k]["args"] == {"bar": [None]}
            assert actual[k]["return"] == [None]
        elif 'example_function' in k:
            assert actual[k]["args"] == {"a": [1, 3], "b": [2, 4], "foo": ["USER_CLASS|foo::Foo", None]}
            assert actual[k]["return"] == [3, 7]


def test_example_function_with_different_args():
    with trace() as actual:
        f = Foo()
        example_function(1, 2, f)
        example_function("bob", "wow", f)
    for k in actual:
        if 'init' in k:
            assert actual[k]["args"] == {"bar": [None]}
            assert actual[k]["return"] == [None]
        elif 'example_function' in k:
            assert actual[k]["args"] == {"a": [1, "bob"], "b": [2, "wow"], "foo": ["USER_CLASS|foo::Foo", "USER_CLASS|foo::Foo"]}
            assert actual[k]["return"] == [3, "bobwow"]


def test_class_method():
    f = Foo()
    with trace() as actual:
        f.get_foo("bob", 9)
    for k in actual:
        assert actual[k]["args"] == {"name": ["bob"], "age": [9]}
        assert actual[k]["return"] == ["bob,9"]


# def test_method_returns_a_class():
#     with trace() as actual:
#         returns_a_class()
#     for k in actual:
#         assert actual[k]["args"] == {"name": ["bob"], "age": [9]}
#         assert actual[k]["return"] == ["bob,9"]

# def test_function_returning_dict():
#     with trace() as actual:
#         function_returning_dict()
#     for k in actual:
#         assert actual[k]["args"] == {}
#         assert actual[k]["return"] == {"dict"}
