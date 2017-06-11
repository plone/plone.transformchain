# -*- coding: utf-8 -*-
from plone.testing.zca import UNIT_TESTING
from plone.transformchain.interfaces import ITransform
from plone.transformchain.interfaces import ITransformer
from plone.transformchain.transformer import Transformer
from plone.transformchain.zpublisher import applyTransformOnSuccess
from zope.component import adapter
from zope.component import provideAdapter
from zope.component import provideUtility
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from ZPublisher.HTTPResponse import default_encoding
from ZPublisher.Iterators import filestream_iterator
from ZServer.FTPRequest import FTPRequest

import os
import tempfile
import unittest


class FauxPubEvent(object):

    def __init__(self, request):
        self.request = request


class IRequestMarker(Interface):
    pass


class IPublishedMarker(Interface):
    pass


class FauxResponse(object):

    def __init__(self, body=''):
        self._body = body
        self.headers = {}

    def getBody(self):
        return self._body

    def setBody(self, body):
        self._body = body


class FauxRequest(dict):

    def __init__(self, published, response=None):
        if response is None:
            response = FauxResponse('<html/>')

        self['PUBLISHED'] = published
        self.response = response
        self.environ = {}


class FauxFTPRequest(FauxRequest, FTPRequest):
    pass


class FauxPublished(object):
    pass


@implementer(ITransform)
@adapter(Interface, Interface)
class FauxTransformBase(object):

    order = 0

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def transformBytes(self, result, encoding):
        return None

    def transformUnicode(self, result, encoding):
        return None

    def transformIterable(self, result, encoding):
        return None


class TestTransformChain(unittest.TestCase):

    layer = UNIT_TESTING

    def setUp(self):
        self.t = Transformer()

    def test_simple(self):

        class Transform1(FauxTransformBase):

            def transformBytes(self, result, encoding):
                return result + ' transformed'

            def transformUnicode(self, result, encoding):
                return result + u' transformed'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' transformed'

        provideAdapter(Transform1, name=u'test.one')

        published = FauxPublished()
        request = FauxRequest(published)
        result = ['Blah']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual('Blah transformed', new_result)

    def test_off_switch(self):

        class Transform1(FauxTransformBase):

            order = 0

            def transformBytes(self, result, encoding):
                return result + ' transformed'

            def transformUnicode(self, result, encoding):
                return result + u' transformed'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' transformed'

        provideAdapter(Transform1, name=u'test.one')

        published = FauxPublished()
        request = FauxRequest(published)
        request.environ['plone.transformchain.disable'] = True

        result = ['Blah']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual(None, new_result)

    def test_ftp_request_not_transformed(self):
        request = FauxFTPRequest(FauxPublished())
        result = ['Blah']
        new_result = self.t(request, result, 'utf8')
        self.assertEqual(None, new_result)

    def test_transform_string(self):

        class Transform1(FauxTransformBase):

            def transformBytes(self, result, encoding):
                return result + ' One'

        provideAdapter(Transform1, name=u'test.one')

        published = FauxPublished()
        request = FauxRequest(published)
        result = 'Blah'
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual('Blah One', new_result)

    def test_transform_unicode(self):

        class Transform1(FauxTransformBase):

            def transformUnicode(self, result, encoding):
                return result + u' One'

        provideAdapter(Transform1, name=u'test.one')

        published = FauxPublished()
        request = FauxRequest(published)
        result = u'Blah'
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual(u'Blah One', new_result)

    def test_transform_iterable(self):

        class Transform1(FauxTransformBase):

            def transformIterable(self, result, encoding):
                return result + [' One']

        provideAdapter(Transform1, name=u'test.one')

        published = FauxPublished()
        request = FauxRequest(published)
        result = ['Blah']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual(['Blah', ' One'], new_result)

    def test_transform_mixed(self):

        class Transform1(FauxTransformBase):

            def transformIterable(self, result, encoding):
                return u''.join(result) + u' One'

        class Transform2(FauxTransformBase):

            order = 1

            def transformUnicode(self, result, encoding):
                return result.encode(encoding) + ' Two'

        class Transform3(FauxTransformBase):

            order = 2

            def transformBytes(self, result, encoding):
                return result.decode(encoding) + u' Three'

        provideAdapter(Transform1, name=u'test.one')
        provideAdapter(Transform2, name=u'test.two')
        provideAdapter(Transform3, name=u'test.three')

        published = FauxPublished()
        request = FauxRequest(published)
        result = ['Blah']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual(u'Blah One Two Three', new_result)

    def test_abort(self):

        class Transform1(FauxTransformBase):
            pass

        provideAdapter(Transform1, name=u'test.one')

        published = FauxPublished()
        request = FauxRequest(published)
        result = ['Blah']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual(['Blah'], new_result)

    def test_abort_chain(self):

        class Transform1(FauxTransformBase):

            def transformBytes(self, result, encoding):
                return 'One'

            def transformUnicode(self, result, encoding):
                return 'One'

            def transformIterable(self, result, encoding):
                return 'One'

        class Transform2(FauxTransformBase):
            pass

        class Transform3(FauxTransformBase):

            order = 2

            def transformBytes(self, result, encoding):
                return result + ' three'

            def transformUnicode(self, result, encoding):
                return result + u' three'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' three'

        provideAdapter(Transform1, name=u'test.one')
        provideAdapter(Transform2, name=u'test.two')
        provideAdapter(Transform3, name=u'test.three')

        published = FauxPublished()
        request = FauxRequest(published)
        result = ['Blah']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual('One three', new_result)

    def test_ordering(self):

        class Transform1(FauxTransformBase):

            order = 100

            def transformBytes(self, result, encoding):
                return result + ' One'

            def transformUnicode(self, result, encoding):
                return result + u' One'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' One'

        class Transform2(FauxTransformBase):

            order = -100

            def transformBytes(self, result, encoding):
                return result + ' Two'

            def transformUnicode(self, result, encoding):
                return result + u' Two'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' Two'

        class Transform3(FauxTransformBase):

            order = 101

            def transformBytes(self, result, encoding):
                return result + ' Three'

            def transformUnicode(self, result, encoding):
                return result + u' Three'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' Three'

        provideAdapter(Transform1, name=u'test.one')
        provideAdapter(Transform2, name=u'test.two')
        provideAdapter(Transform3, name=u'test.three')

        published = FauxPublished()
        request = FauxRequest(published)
        result = ['Initial']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual('Initial Two One Three', new_result)

    def test_request_marker(self):

        class Transform1(FauxTransformBase):

            order = 100

            def transformBytes(self, result, encoding):
                return result + ' One'

            def transformUnicode(self, result, encoding):
                return result + u' One'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' One'

        class Transform2(FauxTransformBase):

            order = -100

            def transformBytes(self, result, encoding):
                return result + ' Two'

            def transformUnicode(self, result, encoding):
                return result + u' Two'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' Two'

        @implementer(ITransform)
        @adapter(Interface, IRequestMarker)
        class Transform3(FauxTransformBase):

            order = 101

            def transformBytes(self, result, encoding):
                return result + ' Three'

            def transformUnicode(self, result, encoding):
                return result + u' Three'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' Three'

        provideAdapter(Transform1, name=u'test.one')
        provideAdapter(Transform2, name=u'test.two')
        provideAdapter(Transform3, name=u'test.three')

        published = FauxPublished()
        request = FauxRequest(published)
        result = ['Initial']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual('Initial Two One', new_result)

        published = FauxPublished()
        request = FauxRequest(published)
        alsoProvides(request, IRequestMarker)
        result = ['Initial']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual('Initial Two One Three', new_result)

    def test_published_marker(self):

        class Transform1(FauxTransformBase):

            order = 100

            def transformBytes(self, result, encoding):
                return result + ' One'

            def transformUnicode(self, result, encoding):
                return result + u' One'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' One'

        class Transform2(FauxTransformBase):

            order = -100

            def transformBytes(self, result, encoding):
                return result + ' Two'

            def transformUnicode(self, result, encoding):
                return result + u' Two'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' Two'

        @implementer(ITransform)
        @adapter(IPublishedMarker, Interface)
        class Transform3(FauxTransformBase):

            order = 101

            def transformBytes(self, result, encoding):
                return result + ' Three'

            def transformUnicode(self, result, encoding):
                return result + u' Three'

            def transformIterable(self, result, encoding):
                return ''.join(result) + ' Three'

        provideAdapter(Transform1, name=u'test.one')
        provideAdapter(Transform2, name=u'test.two')
        provideAdapter(Transform3, name=u'test.three')

        published = FauxPublished()
        request = FauxRequest(published)
        result = ['Initial']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual('Initial Two One', new_result)

        published = FauxPublished()
        alsoProvides(published, IPublishedMarker)
        request = FauxRequest(published)
        result = ['Initial']
        encoding = 'utf-8'

        new_result = self.t(request, result, encoding)
        self.assertEqual('Initial Two One Three', new_result)


class TestZPublisherTransforms(unittest.TestCase):

    UNIT_TESTING

    def setUp(self):
        self.t = Transformer()

    def test_applyTransform_webdav_port(self):

        @implementer(ITransformer)
        class DoNotCallTransformer(object):
            encoding = None

            def __call__(self, request, result, encoding):
                raise AssertionError('Should not have been called')

        transformer = DoNotCallTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        request['WEBDAV_SOURCE_PORT'] = '8081'
        applyTransformOnSuccess(FauxPubEvent(request))

    def test_applyTransform_webdav_method(self):
        @implementer(ITransformer)
        class DoNotCallTransformer(object):
            encoding = None

            def __call__(self, request, result, encoding):
                raise AssertionError('Should not have been called')

        transformer = DoNotCallTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        request['REQUEST_METHOD'] = 'PUT'
        applyTransformOnSuccess(FauxPubEvent(request))

    def test_applyTransform_webdav_pathinfo(self):

        @implementer(ITransformer)
        class DoNotCallTransformer(object):
            encoding = None

            def __call__(self, request, result, encoding):
                raise AssertionError('Should not have been called')

        transformer = DoNotCallTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        request['PATH_INFO'] = '/foo/bar/manage_DAVget'
        applyTransformOnSuccess(FauxPubEvent(request))

    def test_applyTransform_no_utility(self):
        published = FauxPublished()
        request = FauxRequest(published)
        applyTransformOnSuccess(FauxPubEvent(request))

    def test_applyTransform_default_encoding(self):

        @implementer(ITransformer)
        class EncodingCaptureTransformer(object):
            encoding = None

            def __call__(self, request, result, encoding):
                self.encoding = encoding

        transformer = EncodingCaptureTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        applyTransformOnSuccess(FauxPubEvent(request))

        self.assertEqual(default_encoding, transformer.encoding)

    def test_applyTransform_other_encoding(self):
        @implementer(ITransformer)
        class EncodingCaptureTransformer(object):
            encoding = None

            def __call__(self, request, result, encoding):
                self.encoding = encoding

        transformer = EncodingCaptureTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        request.response.headers['content-type'] = 'text/html; charset=dummy'
        applyTransformOnSuccess(FauxPubEvent(request))

        self.assertEqual('dummy', transformer.encoding)

    def test_applyTransform_other_encoding_with_header_missing_space(self):
        @implementer(ITransformer)
        class EncodingCaptureTransformer(object):
            encoding = None

            def __call__(self, request, result, encoding):
                self.encoding = encoding

        transformer = EncodingCaptureTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        request.response.headers['content-type'] = 'text/html;charset=dummy'
        applyTransformOnSuccess(FauxPubEvent(request))

        self.assertEqual('dummy', transformer.encoding)

    def test_applyTransform_str(self):
        @implementer(ITransformer)
        class FauxTransformer(object):

            def __call__(self, request, result, encoding):
                return 'dummystr'

        transformer = FauxTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        applyTransformOnSuccess(FauxPubEvent(request))

        self.assertEqual('dummystr', request.response.getBody())

    def test_applyTransform_unicode(self):
        @implementer(ITransformer)
        class FauxTransformer(object):

            def __call__(self, request, result, encoding):
                return u'dummystr'

        transformer = FauxTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        applyTransformOnSuccess(FauxPubEvent(request))

        # note: the real setBody would encode here
        self.assertEqual(u'dummystr', request.response.getBody())

    def test_applyTransform_iterable(self):
        @implementer(ITransformer)
        class FauxTransformer(object):

            def __call__(self, request, result, encoding):
                return ['iter', 'one']

        transformer = FauxTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        applyTransformOnSuccess(FauxPubEvent(request))

        self.assertEqual('iterone', request.response.getBody())

    def test_applyTransform_streamiterator(self):
        tmp = tempfile.mkstemp()[1]
        try:

            with open(tmp, 'w') as out:
                out.write('foo')

            @implementer(ITransformer)
            class FauxTransformer(object):

                def __call__(self, request, result, encoding):
                    return filestream_iterator(tmp)

            transformer = FauxTransformer()
            provideUtility(transformer)

            published = FauxPublished()
            request = FauxRequest(published)
            applyTransformOnSuccess(FauxPubEvent(request))

            self.assertTrue(
                isinstance(
                    request.response.getBody(),
                    filestream_iterator
                )
            )
        finally:
            os.unlink(tmp)

    def test_applyTransform_str_input_body(self):
        @implementer(ITransformer)
        class FauxTransformer(object):

            def __call__(self, request, result, encoding):
                assert isinstance(result, list)
                assert isinstance(result[0], str)
                return 'dummystr'

        transformer = FauxTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        request.response.setBody('<html />')

        applyTransformOnSuccess(FauxPubEvent(request))

        # note: the real setBody would encode here
        self.assertEqual('dummystr', request.response.getBody())

    def test_applyTransform_unicode_input_body(self):
        @implementer(ITransformer)
        class FauxTransformer(object):

            def __call__(self, request, result, encoding):
                assert isinstance(result, list)
                assert isinstance(result[0], str)
                return u'dummystr'

        transformer = FauxTransformer()
        provideUtility(transformer)

        published = FauxPublished()
        request = FauxRequest(published)
        request.response.setBody(u'<html />')

        applyTransformOnSuccess(FauxPubEvent(request))

        # note: the real setBody would encode here
        self.assertEqual(u'dummystr', request.response.getBody())
