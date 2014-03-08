__author__ = 'cole'


class FunctionAsClass(object):
    def __init__(self, name, fn=None):
        self.name = name
        self.arg_names = [self.name]
        self.fn = fn

    def __getattr__(self, key, ref=None):
        self.key = F(key)
        self.arg_names.append(self.key.name)

        if key == 'res':
            _res = self.fn(*self.arg_names[:-1])
            self.res = _res
            return _res

        return self


FasC = FunctionAsClass