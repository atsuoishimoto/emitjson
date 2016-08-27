from .models import *
from django.test import TestCase
import emitjson
from django.db.models.fields.related import ForeignObjectRel

##
##from django.db.models.fields.related import ManyToManyField
##opts = instance._meta
##data = {}
##for f in chain(opts.concrete_fields, opts.virtual_fields, opts.many_to_many):
##    if not getattr(f, 'editable', False):
##        continue
##    if fields and f.name not in fields:
##        continue
##    if exclude and f.name in exclude:
##        continue
#
#def get_all_field_names(model):
#    from itertools import chain
#    return list(set(chain.from_iterable(
#        (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
#        for field in model._meta.get_fields()
#            if not isinstance(field, ForeignObjectRel)
#    )))

class EJTest(TestCase):
    def test_model1(self):
        repo = emitjson.repository()
        repo.fromDjangoModel(Model1, attrs={}, ignores={})
        repo.fromDjangoModel(Model2, attrs={}, ignores={})

        m1 = Model1(charattr='test', intattr=100)
        m1.save()

        assert repo(m1) == {'charattr': 'test', 'intattr': 100, 'id': 1}

        m2 = Model2(charattr='test', model1=m1)
        m2.save()

        assert repo(m2) == {'charattr': 'test', 'model1_id': 1, 'id': 1,
            'model1': {'charattr': 'test', 'intattr': 100, 'id': 1}}

    def test_model2(self):
        repo = emitjson.repository()

        @repo.register(Model1)
        class Model1Converter(emitjson.DjangoModelConverter):
            pass

        @repo.register(Model2)
        class Model2Converter(emitjson.DjangoModelConverter):
            pass

        m1 = Model1(charattr='test', intattr=100)
        m1.save()

        assert repo(m1) == {'charattr': 'test', 'intattr': 100, 'id': 1}

        m2 = Model2(charattr='test', model1=m1)
        m2.save()

        assert repo(m2) == {'charattr': 'test', 'model1_id': 1, 'id': 1,
            'model1': {'charattr': 'test', 'intattr': 100, 'id': 1}}
