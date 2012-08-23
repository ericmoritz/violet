An experimental Python DSL for validation

Usage:

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

