An experimental Python DSL for validation

## Usage:

Here is an example of the use of Violet:

    from violet import is_type, cast, passes
    validator = is_type(
        [
            {
                "name": is_type(str) & passes(len),
                "age": cast(int) & passes(lambda x: 18 <= x <= 99),
                "sex": cast(str.lower) & passes(lambda s: s in ["male", "female"])
                }
            ])
        
    data = [{'name': 'Sue', 'age': '28', 'sex': 'FEMALE'},
            {'name': 'Sam', 'age': '42', 'sex': 'Male'},
            {'name': 'Sacha', 'age': '20', 'sex': 'Male'}]

    assert [{'name': 'Sue', 'age': 28, 'sex': 'female'},
            {'name': 'Sam', 'age': 42, 'sex': 'male'},
            {'name': 'Sacha', 'age': 20, 'sex': 'male'}] == validator(data)

## Concept

The idea behind violet is to create a composition of directives using
the & and | operators as well as container types.

There are currently three directives, `is_type`, `cast` and `passes`.

### is_type

This directive raises a `TypeError` if the type check fails.  

Possible arguments for `is_type` are `type` classes such as `int`, `str`,
`float`, etc:

    validator = is_type(int)
    assert 10 == validator(10)

    validator = is_type(str)
    assert "foo" == validator("foo")

Constant values:

    validator = is_type(10)
    assert 10 == validator(10)

Other directives and composites of those directives:

    validator = is_type(is_type(int) | is_type(str))
    assert 10 == validator(10)
    assert "foo" == validator("foo")

    validator = is_type(cast(int) & passes(lambda x: x > 10))
    assert 11 == validator("11")


Containers of types or directives:

    # list
    validator = is_type([int])
    assert [10, 11, 12] == validator([10, 11, 12])

    # set
    validator = is_type({int})
    assert {10, 11, 12} == validator({10, 11, 12})

    # dict
    validator = is_type({"name": str, "age": int})
    assert {"name": "Eric", "age": 32} == validator({"name": "Eric", "age": 32})

    validator = is_type({"name": str, "age": is_type(cast(int))})
    assert {"name": "Eric", "age": 32} == validator({"name": "Eric", "age": "32"})

    # nested containers
    validator = is_type({"name": str, "friends": {str}})

    assert {"name": "Eric", "friends": {"Glenn", "Mark"}}
      == validator({"name": "Eric", "friends": {"Glenn", "Mark"}})

    
### cast(function)

Simply converts the value as another:

    validator = cast(int)
    assert 10 = validator("10")

### passes(predicate)

Raises an `AssertionError` if the predicate returns False,
passes the value through if the predicate returns True:

    validator = passes(lambda x: x > 10)
    assert 11 = validator(11)

## Not implemented

Currently there is no way to support optional keys in dictionary
types.  If a key is not found in the value being validated, a
`KeyError` is currently raised.  Support for optional keys is a
planned feature.
