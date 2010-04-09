Introduction
============

This package provides a means of modifying the response from a page published
with ``repoze.zope2`` or the "classic" ``ZPublisher`` before it is returned to
the browser.

Register a uniquely named adapter from ``(published, request)`` providing
the ``ITransform`` interface. ``published`` is the published object, e.g. a
view; ``request`` is the current request.

The order of the transforms can be maintained using the ``order`` property of
the adapter.

One of three methods will be called, depending on what type of input was
obtained from the publisher and/or the previous method.

  * transformBytes() is called if the input is a str (bytes) object
  * transformUnicode() is called if the input is a unicode object
  * transformIterable() is called if the input is another type of iterable

Each stage can return a byte string, a unicode string, or an iterable.

Most transformers will have a "natural" representation of the result, and will
implement the respective method to return another value of the same
representation, e.g. implement transformUnicode() to transform and return a
unicode object. The other methods may then either be implemented to return
None (do nothing) or convert the value to the appropriate type.

The first transformer in the chain is likely to get:

  * A byte string if the transformer is running under the standard Zope 2
    ZPublisher.
  * An iterable if the transformer is running under repoze.zope2 or another
    WSGI pipeline.

Check ``self.request.response.getHeader('content-type')`` to see the type of
result. The iterable, when unwound, will conform to this type, e.g. for
text/html, ``''.join(result)`` should be an HTML string.

The return value is passed to the next transform in the chain. The final
transform should return a unicode string, an encoded string, or an iterable.

If a byte string or unicode string is returned by the last transform in the
chain, the ``Content-Length`` header will be automatically updated

Return ``None`` to signal that the result should not be changed from the
previous transform.

Here is an example that uppercases everything::

    from zope.interface import implements, Interface
    from zope.component import adapts
    
    from plone.transformchain.interfaces import ITransform

    class UpperTransform(object):
        implements(ITransform)
        adapts(Interface, Interface) # any context, any request
        
        order = 1000
        
        def __init__(self, published, request):
            self.published = published
            self.request = request
        
        def transformBytes(self, result, encoding):
            return result.upper()
            
        def transformUnicode(self, result, encoding):
            return result.upper()
        
        def transformIterable(self, result, encoding):
            return [s.upper() for s in result]

You could register this in ZCML like so::

    <adapter factory=".transforms.UpperTransform" name="example.uppertransform" />

If you need to turn off transformations for a particular request, you can 
set a key in ``request.environ``::

    request.environ['plone.transformchain.disable'] = True

This will leave the response untouched and will not invoke any
``ITransform`` adapters at all.
