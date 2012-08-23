class Composable(object):
    def __and__(self, other):
        return _and(self, other)

    def __or__(self, other):
        return _or(self, other)


class _and(Composable):
    def __init__(self, first, second):
        self.first, self.second = first, second

    def __call__(self, val):
        return self.second(self.first(val))


class _or(Composable):
    def __init__(self, first, second):
        self.first, self.second = first, second

    def __call__(self, val):
        try:
            return self.first(val)
        except Exception, e1:
            return self.second(val)
        

class passes(Composable):
    def __init__(self, predicate):
        self.predicate = predicate

    def __call__(self, value):
        assert self.predicate(value)
        return value


class is_type(Composable):
    def __init__(self, Type):
        self.type = Type
        
    def __call__(self, value):
        if isinstance(self.type, type) and isinstance(value, self.type):
            return value
        # constant test
        elif self.type == value:
            return value
        # container check
        elif isinstance(self.type, list):
            # assert that the value is a list
            is_type(list)(value)

            # validate each item
            validator = _compose_validators(_or, self.type)
            accum = []
            for item in value:
                accum.append(validator(item))
            return accum

        elif isinstance(self.type, set):
            # asset that the value is a set
            is_type(set)(value)
            
            # validate each item
            validator = _compose_validators(_or, list(self.type))
            accum = set()
            for x in value:
                accum.add(validator(x))
            return accum
        elif isinstance(self.type, dict):
            accum = {}
            for key, subtype in self.type.iteritems():
                subvalidator = _ensure_validator(subtype)
                accum[key] = subvalidator(value[key])
            return accum
        else:
            raise TypeError("%r is not of type %s" % (value, type))


class cast(Composable):
    def __init__(self, caster):
        self.caster = caster

    def __call__(self, value):
        return self.caster(value)


def _ensure_validator(item):
    if isinstance(item, Composable):
        return item
    else:
        return is_type(item)


def _compose_validators(composer, validators):
    return reduce(lambda x,y: composer(x, _ensure_validator(y)),
                  validators[1:],
                  _ensure_validator(validators[0]))
        
