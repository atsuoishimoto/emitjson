from functools import singledispatch
from collections import abc
import itertools
import datetime


def repository():
    @singledispatch
    def _repogitory(obj):
        return obj

    def _register(cls, func=None):
        if func is None:
            return lambda f: _register(cls, f)

        if isinstance(func, type):
            if issubclass(func, ObjConverter):
                func = func(cls)

        if isinstance(func, ObjConverter):
            func.repogitory = _repogitory
            func = func.run

        return _repogitory.org_register(cls, func)

    _repogitory.org_register = _repogitory.register
    _repogitory.register = _register

    def fromSQLAlchemyModel(model, attrs=None, ignores=None):
        names = [col.name for col in model.__table__.columns]
        ObjConverter.build(_repogitory, model, names, attrs, ignores)

    _repogitory.fromSQLAlchemyModel = fromSQLAlchemyModel

    def fromDjangoModel(model, attrs, ignore):
        ObjConverter.build(_repogitory, model, model._meta.get_all_field_names(),
                    attrs, ignores)
    _repogitory.fromDjangoModel = fromDjangoModel

    def raw(obj):
        return obj
    _repogitory.register(str, raw)

    def conv_seq(obj):
        return tuple(_repogitory(o) for o in obj)

    _repogitory.register(abc.Sequence, conv_seq)
    _repogitory.register(abc.Set, conv_seq)

    @_repogitory.register(abc.Mapping)
    def conv_mapping(obj):
        return {_repogitory(k):_repogitory(v) for k, v in obj.items()}

    def conv_date(obj):
        return obj.isoformat()
    _repogitory.register(datetime.date, conv_date)
    _repogitory.register(datetime.datetime, conv_date)

    return _repogitory


class attr:
    def __init__(self, attrname=None, map=None):
        self.attrname = attrname
        self.map = map

    def convert(self, obj, name):
        if self.attrname:
            name = self.attrname
        ret = getattr(obj, name)
        if self.map:
            ret = self.map(ret)
        return ret

class ObjConverter:
    @classmethod
    def build(cls, repo, target, names, attrs, ignores):
        _attrs = {name:attr for name in names}
        if attrs:
            _attrs.update(attrs)
        if ignores:
            for name in ignores:
                if name in _attrs:
                    del _attrs[name]

        f = cls(target, attrs=_attrs)
        repo.register(target, f)
        return f

    def _init_args(self, target):
        return {}

    def __init__(self, target, *, attrs=None, ignores=()):
        self.target = target
        self.attrs = self._init_args(target)

        for name, value in self.__class__.__dict__.items():
            if isinstance(value, type):
                if issubclass(value, attr):
                    value = value()
            if isinstance(value, attr):
                self.attrs[name] = value

        if attrs:
            for name, value in attrs.items():
                if isinstance(value, type):
                    if issubclass(value, attr):
                        value = value()
                self.attrs[name] = value

        for n in itertools.chain(ignores, getattr(self, 'IGNORES', ())):
            if n in self.attrs:
                del self.attrs[n]

    def on_convert(self, obj, values):
        for name, f in self.attrs.items():
            values[name] = f.convert(obj, name)

    def run(self, obj):
        values = {}
        self.on_convert(obj, values)
        return self.repogitory(values)


class SAModelConverter(ObjConverter):
    def _init_args(self, target):
        names = [col.name for col in target.__table__.columns]
        return {name:attr() for name in names}

