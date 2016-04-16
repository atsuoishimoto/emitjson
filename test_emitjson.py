from emitjson import repository, ObjConverter, attr
import datetime, base64


myrepo = repository()


def test_converter():
    s = myrepo([1, '222', {3:{4}}])
    assert s == (1, '222', {3: (4,)})


def test_date():
    d = datetime.datetime.now()
    assert d.isoformat() == myrepo(d)


@myrepo.register(bytes)
def conv_bytes(obj):
    # encode bytes object in Base64 format
    return base64.b64encode(obj).decode('ascii')


def test_override():
    ret = myrepo(b'abcdefg')
    assert 'YWJjZGVmZw==' == ret


class Class1:
    def __init__(self):
        self.prop1 = 'spam'
        self.prop2 = 'ham'


class Class2:
    def __init__(self):
        self.prop3 = [Class1()]


@myrepo.register(Class1)
class Class1Converter(ObjConverter):
    prop1 = attr
    prop2 = attr(map=lambda o:o.upper())


@myrepo.register(Class2)
class Class2Converter(ObjConverter):
    prop_x = attr('prop3')


def test_class():
    ret = myrepo(Class2())
    assert ret == {'prop_x': ({'prop2': 'HAM', 'prop1': 'spam'},)}

