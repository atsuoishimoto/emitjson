import datetime, base64, pytest
from emitjson import repository, ObjConverter, attr, SAModelConverter

try:
    import sqlalchemy
    has_sqlalchemy = True
except ImportError:
    has_sqlalchemy = False

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


class Class3:
    def __init__(self):
        self.prop = 1


@myrepo.register(Class3)
class Class3Converter(ObjConverter):
    def on_convert(self, obj, values):
        super().on_convert(obj, values)
        values['dynamic_prop'] = obj.prop

def test_customize():
    ret = myrepo(Class3())
    assert ret == {'dynamic_prop': 1}


def sa_model():
    from sqlalchemy import create_engine, Table, Column, Integer
    from sqlalchemy.ext.declarative import declarative_base

    engine = create_engine('sqlite:///:memory:')
    Base = declarative_base()

    class Test(Base):
        __tablename__ = 'test'
        a = Column(Integer, primary_key=True)
        b = Column(Integer)
        c = Column(Integer)
        d = Column(Integer)

    Base.metadata.create_all(engine)
    return Test

@pytest.mark.skipif(not has_sqlalchemy, reason='SQLAlchemy is not installed')
def test_alchemy1():
    Test = sa_model()

    myrepo.fromSQLAlchemyModel(Test, attrs={'bbb':attr('b')}, ignores=['b'])
    ret = myrepo(Test(a=1, b=2, c=3, d=4))
    assert ret == {'a': 1, 'bbb': 2, 'c': 3, 'd': 4}


@pytest.mark.skipif(not has_sqlalchemy, reason='SQLAlchemy is not installed')
def test_alchemy_decls():
    Test = sa_model()

    @myrepo.register(Test)
    class SA(SAModelConverter):
        IGNORES = ['b', 'c']
        prop2 = attr(attrname='b', map=lambda o:o*3)

    ret = myrepo(Test(a=1, b=2, c=3, d=4))
    assert ret == {'a': 1, 'd': 4, 'prop2': 6}
