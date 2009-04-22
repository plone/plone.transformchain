Introduction
============

This package provides a means of modifying the response from a page published
with repoze.zope2 (only) before it is returned to the browser.

Register a uniquely named adapter from (published, request) providing
the ITransform interface. published is the published object, e.g. a view;
request is the current request.

The order of the transforms can be maintained using the 'order' property of
the adapter.

The __call__() method is passed an iterable 'result' and the current encoding.
Check self.request.response.getHeader('content-type') to see the type of
result. The iterable, when unwound, will conform to this type, e.g. for
text/html, ''.join(result) should be an HTML string.

The return value is passed to the next transform in the chain. The final
transform should return a unicode string, an encoded string, or an iterable.
If a string is returned, the 'Content-Length' header will be automatically
updated.

Return None to signal that the result should not be changed from the previous
transform.