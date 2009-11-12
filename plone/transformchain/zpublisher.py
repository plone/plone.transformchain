import sys
import re

from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.component import queryUtility, adapter

from ZPublisher.Iterators import IStreamIterator
from ZPublisher.HTTPResponse import default_encoding

from plone.transformchain.interfaces import ITransformer

from ZPublisher.interfaces import IPubBeforeCommit

try:
    from ZPublisher.interfaces import IPubBeforeAbort
except ImportError:
    # old Zope 2.12 or old ZPublisherBackport - this interface won't be
    # used, most likely, so the effect is that error messages aren't styled.
    class IPubBeforeAbort(Interface):
        pass
    
CHARSET_RE = re.compile(r'(?:application|text)/[-+0-9a-z]+\s*;\scharset=([-_0-9a-z]+)(?:(?:\s*;)|\Z)', re.IGNORECASE)

def extractEncoding(response):
    """Get the content encoding for the response body
    """
    encoding = default_encoding
    ct = response.headers.get('content-type')
    if ct:
        match = CHARSET_RE.match(ct)
        if match:
            encoding = match.group(1)
    return encoding

def isEvilWebDAVRequest(request):
    if request.get('WEBDAV_SOURCE_PORT', None):
        return True
    
    if request.get('REQUEST_METHOD', 'GET').upper() not in ('GET', 'POST',):
        return True
    
    if request.get('PATH_INFO', '').endswith('manage_DAVget'):
        return True

    return False

def applyTransform(request, body=None):
    """Apply any transforms by delegating to the ITransformer utility
    """
    
    if isEvilWebDAVRequest(request):
        return
    
    transformer = queryUtility(ITransformer)
    if transformer is not None:
        response = request.response
        encoding = extractEncoding(response)
        
        if body is None:
            body = response.getBody()
        
        result = body
        if isinstance(result, basestring):
            result = [result]
        
        transformed = transformer(request, result, encoding)
        if transformed is not None and transformed is not result:
            
            # horrid check to deal with Plone 3/Zope 2.10, where this is still an old-style interface
            if ((IInterface.providedBy(IStreamIterator)     and IStreamIterator.providedBy(transformed))
             or (not IInterface.providedBy(IStreamIterator) and IStreamIterator.isImplementedBy(transformed))
            ):
                request.response.setBody(transformed)
            # setBody() can deal with byte and unicode strings (and will encode as necessary)...
            elif isinstance(transformed, basestring):
                request.response.setBody(transformed)
            # ... but not with iterables
            else:
                request.response.setBody(''.join(transformed))

@adapter(IPubBeforeCommit)
def applyTransformOnSuccess(event):
    """Apply the transform after a successful request
    """
    applyTransform(event.request)

@adapter(IPubBeforeAbort)
def applyTransformOnFailure(event):
    """Apply the transform to the error html output
    """
    if not event.retry:
        request = event.request
        exc_info = sys.exc_info()
        error = exc_info[1]
        if isinstance(error, basestring): # Plone 3.x / Zope 2.10
            newBody = applyTransform(request, error)
            if newBody is not None:
                # If it's any consolation, Laurence felt quite dirty doing this...
                raise exc_info[0], newBody, exc_info[2]
        else: # plone 4
            applyTransform(request)
