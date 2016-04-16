============================
emitjson
============================

Help composing objects to emit JSON.

``emitjson.repository()`` creates a standard `single-dispatch generic function <http://docs.python.org/3/library/functools.html#functools.singledispatch>`_ to covert objects to JSON-friendly objects. ``repository()`` converts some object types that are not supported by `json module` such as ``set()`` or ``datetime.datetime()``.

You can also add your own converters as `singledispatch function <http://docs.python.org/3/library/functools.html#functools.singledispatch>`_.

::

    import emitjson
    import base64

    my_repo = emitjson.repository()  # create emitjson repository

    @myrepo.register(bytes)
    def conv_bytes(obj):
        # encode bytes object in Base64 format
        return base64.b64encode(obj).decode('ascii')

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


@emitjson.repository
--------------------

Returns a `single-dispatch generic function <http://docs.python.org/3/library/functools.html#functools.singledispatch>`_ instance.

``emitjson.repository()`` overrides following types by default.

- ``collections.abc.Sequence`` objects are converted to ``tuple``. Elements in the sequence are converted recursively.

- Keys and values of the ``collections.abc.Mapping`` are converted recursively.

- ``datetime.date`` and ``datetime.datetime`` objects are converted to `isoformat()` string.



emitjson.ObjConverter class
----------------------------------

``emitjson.ObjConverter`` class defines a converter from arbitrary objects to dictionary.

You can register field names of the target object. If an attribute of the ``ObjConverter`` is ``emitjson.attr`` class, converter gets a value from attribute in the same name from the target object. If an attribute is an instance of ``attr`` class, converter gets a value from the attribute specified in the ``attr`` object.

emitjson.attr class
--------------------

Specify name of attribute to get value. The attribute name to get value could be supplied as arguments of ``attr``. See above for examples.

``attr`` also accepts ``map`` argument which is a functon to convert a target object to arbitrary objects.

Resulting dict objects are also converted recursively.


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


