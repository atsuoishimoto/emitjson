from functools import singledispatch
from collections import abc
import datetime




def build_converter(repo, cls, attrs):
    f = ObjConverter(None, attrs)
    repo.register(cls, f)


def _from_model(repo, model, names, attrs, ignores):
    _attrs = {name:attr for name in names}
    if attrs:
        _attrs.update(attrs)
    if ignores:
        for name in ignores:
            if name in _attrs:
                del _attrs[name]

    build_converter(repo, model, _attrs)


def repository():
    @singledispatch
    def converter(obj):
        return obj

    def _register(cls, func=None):
        if func is None:
            return lambda f: _register(cls, f)

        if isinstance(func, type):
            if issubclass(func, ObjConverter):
                func = func(converter).convert
        elif isinstance(func, ObjConverter):
            func.converter = converter
            func = func.convert
        return converter.org_register(cls, func)

    converter.org_register = converter.register
    converter.register = _register

    def fromSQLAlchemyModel(model, attrs=None, ignores=None):
        names = [col.name for col in model.__table__.columns]
        _from_model(converter, model, names, attrs, ignores)

    converter.fromSQLAlchemyModel = fromSQLAlchemyModel


    def fromDjangoModel(model, attrs, ignore):
        _from_model(converter, model, model._meta.get_all_field_names(), attrs, ignores)

    converter.fromDjangoModel = fromDjangoModel


    def raw(obj):
        return obj

    converter.register(str, raw)

    def conv_seq(obj):
        return tuple(converter(o) for o in obj)

    converter.register(abc.Sequence, conv_seq)
    converter.register(abc.Set, conv_seq)

    @converter.register(abc.Mapping)
    def conv_mapping(obj):
        return {converter(k):converter(v) for k, v in obj.items()}

    def conv_date(obj):
        return obj.isoformat()

    converter.register(datetime.date, conv_date)
    converter.register(datetime.datetime, conv_date)

    return converter


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
    def __init__(self, converter, attrs=None):
        self.converter = converter
        self.attrs = {}
        if attrs:
            for name, value in attrs.items():
                if isinstance(value, type):
                    if issubclass(value, attr):
                        value = value()
                self.attrs[name] = value

        for name, value in self.__class__.__dict__.items():
            if isinstance(value, type):
                if issubclass(value, attr):
                    value = value()
            if isinstance(value, attr):
                self.attrs[name] = value

    def convert(self, obj):
        ret = {}
        for name, f in self.attrs.items():
            ret[name] = f.convert(obj, name)
        return self.converter(ret)
