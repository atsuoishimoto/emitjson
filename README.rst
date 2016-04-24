============================
emitjson
============================

Help composing objects to emit JSON.

``emitjson.repository()`` creates a repository of functions to convert various type of objects to JSON-friendly objects. The repository is a `single-dispatch generic function <http://docs.python.org/3/library/functools.html#functools.singledispatch>`_  that returns a converted object if the converter for the type is registered.

The repository contains some default converters for types that are not supported by `json module` such as ``set()`` or ``datetime.datetime()``. Also, default repository returns (shallow) copies of standard container types such as ``collections.abc.Mapping`` or ``collection.abc.Sequence``. Items in the container object are also converted recursively.

::

    >>> import datetime
    >>> import emitjson
    >>> my_repo = emitjson.repository()  # create emitjson repository
    >>> src = [1, 2, datetime.datetime.now(), {4, 5, 6}]
    >>> new = my_repo(src)
    >>> print(new)
    (1, 2, '2016-04-20T22:09:18.731157', (4, 5, 6))


You can add your own converters as `singledispatch function <http://docs.python.org/3/library/functools.html#functools.singledispatch>`_. Following example add a converter to generate Base64 strings from ``bytes`` objects.

::

    >>> import emitjson
    >>> import base64
    >>> my_repo = emitjson.repository()  # create emitjson repository
    >>> @my_repo.register(bytes)
    >>> def conv_bytes(obj):
    ...    # encode bytes object in Base64 format
    ...    return base64.b64encode(obj).decode('ascii')
    ...
    >>> print(my_repo([b'abcd']))
    ('YWJjZA==', )

You can also define mapper class to convert objects to dictionary.

::

    from emitjson repository, attr, ObjConverter

    class Class1:
        def __init__(self):
            self.prop1 = 'spam'
            self.prop2 = 'ham'

    class Class2:
        def __init__(self):
            self.prop3 = [Class1()]


    my_repo = emitjson.repository()  # create emitjson repository

    @my_repo.register(Class1)
    class Class1Converter(ObjConverter):
        prop1 = attr    # get obj.prop1
        prop2 = attr    # get obj.prop2

    @my_repo.register(Class2)
    class Class2Converter(ObjConverter):
        prop_x = attr('prop3')  # get obj.prop3 but store as 'prop_x'

Requirements
============

* Python 3.4 or later


Functions
=============


@repository()
------------------------

Create a repository of object converters. The repository is an instance of the `single-dispatch generic function <http://docs.python.org/3/library/functools.html#functools.singledispatch>`_.

The repository overrides following types by default.

- ``collections.abc.Sequence`` objects are converted to ``tuple``. Elements in the sequence are converted recursively.

- Keys and values of the ``collections.abc.Mapping`` are converted recursively.

- ``datetime.date`` and ``datetime.datetime`` objects are converted to ``isoformat()`` string.



ObjConverter class
----------------------------------

``ObjConverter`` class create a converter from an arbitrary object to a dictionary. Values obtained from objects are also converted recursively.

Attribute names to be converted are defined as ``attr`` class members of ``ObjConverter`` class.

If an attribute of the ``ObjConverter`` is an instance of ``attr``, `attrname` arguments specifies attribute name to be converted.

Resulting dict objects are also converted recursively.

ObjConverter.on_convert(obj, values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``on_convert`` method is called to obtain attribute of ``obj`` and store the value to the ``values`` dictionary. You can override ``on_convert()`` method to customize conversion.

::

    class Class3:
        prop = 1

    @myrepo.register(Class3)
    class Class3Converter(ObjConverter):
        def on_convert(self, obj, values):
            super().on_convert(obj, values)
            values['dynamic_prop'] = obj.prop

    print(myrepo(Class3())  # prints {'dynamic_prop': 1}


attr(attrname=None, map=None) class
---------------------------------------------

Converts an attribute of object.  

``attrname`` overrides the attribute name if not omitted.

``map`` argument which is a functon to convert a target object to arbitrary objects.


SAModelConverter class
---------------------------------

``SAModelConverter`` class create a converter from an SQLAlchemy model. Columns of the model are converted unless specified in ``IGNORES`` member of the class.

::

    class Test(Base):
        __tablename__ = 'test'
        a = Column(Integer, primary_key=True)
        b = Column(Integer)
        c = Column(Integer)
        d = Column(Integer)

    @myrepo.register(Test)
    class TestModelConverter(SAModelConverter):
        IGNORES = ('c', 'd')    # ommit Test.c and Test.d


repository.fromSQLAlchemyModel(model, attrs=None, ignores=None)
------------------------------------------------------------------

Another way to register a converter of SQLAlchemy model. Columns of the model are converted unless the name of column is listed in ``ignore`` argument. ``attrs`` is a dictionary of key name and ``attr`` object. 

::

    # Converts Test model
    myrepo.fromSQLAlchemyModel(Test,
        attrs={
            'fld1': attr,           # Emits Test.fld1 as value of 'fld1'
            'X_VALUE':attr('fld_X') # Emits Test.fld_X as value of 'X_VALUE'
        },
        ignores=('fld3', 'fld4')) # ignore Test.fld3 and Test.fld2


Copyright 
=========================

Copyright (c) 2016 Atsuo Ishimoto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
