# -*- coding: utf-8 -*-
from plone.transformchain.interfaces import ITransformer
from zope.component import adapter
from zope.component import queryUtility
from zope.interface import Interface
from ZPublisher.HTTPResponse import default_encoding
from ZPublisher.interfaces import IPubBeforeCommit
from ZPublisher.Iterators import IStreamIterator

import re


try:
    from ZPublisher.interfaces import IPubBeforeAbort
except ImportError:
    # old Zope 2.12 or old ZPublisherBackport - this interface won't be
    # used, most likely, so the effect is that error messages aren't styled.
    class IPubBeforeAbort(Interface):
        pass

CHARSET_RE = re.compile(
    r'(?:application|text)/[-+0-9a-z]+\s*;\s?charset=([-_0-9a-z]+)'
    r'(?:(?:\s*;)|\Z)',
    re.IGNORECASE
)


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
        return None

    transformer = queryUtility(ITransformer)
    if transformer is not None:
        response = request.response
        encoding = extractEncoding(response)

        if body is None:
            body = response.getBody()

        result = body
        if isinstance(result, str):
            result = [result]
        elif isinstance(result, unicode):
            result = [result.encode(encoding)]

        transformed = transformer(request, result, encoding)
        if transformed is not None and transformed is not result:
            return transformed

    return None


@adapter(IPubBeforeCommit)
def applyTransformOnSuccess(event):
    """Apply the transform after a successful request
    """
    transformed = applyTransform(event.request)
    if transformed is None:
        return
    response = event.request.response

    if IStreamIterator.providedBy(transformed):
        response.setBody(transformed)
    # setBody() can deal with byte and unicode strings (and will encode as
    # necessary)...
    elif isinstance(transformed, basestring):
        response.setBody(transformed)
    # ... but not with iterables
    else:
        response.setBody(''.join(transformed))


@adapter(IPubBeforeAbort)
def applyTransformOnFailure(event):
    """Apply the transform to the error html output
    """
    if event.retry:
        return
    # response.status might still be 200 because
    # IPubBeforeAbort is notified before
    # ZPublisher.Publish.publish_module_standard
    # calls HTTPResponse.exception()
    # which actually updates the status
    setErrorStatusOnResponse(event)
    applyTransformOnSuccess(event)


def setErrorStatusOnResponse(event):
    error_class = event.exc_info[0]
    event.request.response.setStatus(error_class)
