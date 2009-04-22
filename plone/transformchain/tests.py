import unittest

from zope.interface import Interface, implements, alsoProvides
from zope.component import adapts, provideAdapter
from zope.app.testing.placelesssetup import PlacelessSetup

from plone.transformchain.interfaces import ITransform
from plone.transformchain.handler import Transformer

class IRequestMarker(Interface):
    pass

class IPublishedMarker(Interface):
    pass

class FauxRequest(dict):
    
    def __init__(self, published):
        self['PUBLISHED'] = published

class FauxPublished(object):
    pass

class TestTransformChain(unittest.TestCase, PlacelessSetup):
    
    def setUp(self):
        PlacelessSetup.setUp(self)
        self.t = Transformer()

    def tearDown(self):
        PlacelessSetup.tearDown(self)
        
    def test_simple(self):
        
        class Transform1(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 0
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                return ''.join(result) + " transformed"
        
        provideAdapter(Transform1, name=u"test.one")
        
        published = FauxPublished()
        request = FauxRequest(published)
        result = ["Blah"]
        encoding = 'utf-8'
        
        new_result = self.t(request, result, encoding)
        self.assertEquals("Blah transformed", new_result)
    
    def test_abort(self):
        
        class Transform1(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 0
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                return None
        
        provideAdapter(Transform1, name=u"test.one")
        
        published = FauxPublished()
        request = FauxRequest(published)
        result = ["Blah"]
        encoding = 'utf-8'
        
        new_result = self.t(request, result, encoding)
        self.assertEquals(["Blah"], new_result)

    def test_abort_chain(self):
        
        class Transform1(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 0
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                return "One"
        
        class Transform2(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 1
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                return None
                
        class Transform3(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 2
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                return result + " three"
        
        provideAdapter(Transform1, name=u"test.one")
        provideAdapter(Transform2, name=u"test.two")
        provideAdapter(Transform3, name=u"test.three")
        
        published = FauxPublished()
        request = FauxRequest(published)
        result = ["Blah"]
        encoding = 'utf-8'
        
        new_result = self.t(request, result, encoding)
        self.assertEquals("One three", new_result)
        
    def test_ordering(self):
        
        class Transform1(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 100
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "One"
        
        class Transform2(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = -100
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "Two"
                
        class Transform3(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 101
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "Three"
        
        provideAdapter(Transform1, name=u"test.one")
        provideAdapter(Transform2, name=u"test.two")
        provideAdapter(Transform3, name=u"test.three")
        
        published = FauxPublished()
        request = FauxRequest(published)
        result = ["Initial"]
        encoding = 'utf-8'
        
        new_result = self.t(request, result, encoding)
        self.assertEquals("InitialTwoOneThree", new_result)
    
    def test_request_marker(self):
        
        class Transform1(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 100
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "One"
        
        class Transform2(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = -100
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "Two"
                
        class Transform3(object):
            implements(ITransform)
            adapts(Interface, IRequestMarker)
            
            order = 101
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "Three"
        
        provideAdapter(Transform1, name=u"test.one")
        provideAdapter(Transform2, name=u"test.two")
        provideAdapter(Transform3, name=u"test.three")
        
        published = FauxPublished()
        request = FauxRequest(published)
        result = ["Initial"]
        encoding = 'utf-8'
        
        new_result = self.t(request, result, encoding)
        self.assertEquals("InitialTwoOne", new_result)
        
        published = FauxPublished()
        request = FauxRequest(published)
        alsoProvides(request, IRequestMarker)
        result = ["Initial"]
        encoding = 'utf-8'
        
        new_result = self.t(request, result, encoding)
        self.assertEquals("InitialTwoOneThree", new_result)
    
    def test_published_marker(self):
        
        class Transform1(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = 100
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "One"
        
        class Transform2(object):
            implements(ITransform)
            adapts(Interface, Interface)
            
            order = -100
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "Two"
                
        class Transform3(object):
            implements(ITransform)
            adapts(IPublishedMarker, Interface)
            
            order = 101
            
            def __init__(self, published, request):
                self.published = published
                self.request = request
            
            def __call__(request, result, encoding):
                if not isinstance(result, str): result = ''.join(result)
                return result + "Three"
        
        provideAdapter(Transform1, name=u"test.one")
        provideAdapter(Transform2, name=u"test.two")
        provideAdapter(Transform3, name=u"test.three")
        
        published = FauxPublished()
        request = FauxRequest(published)
        result = ["Initial"]
        encoding = 'utf-8'
        
        new_result = self.t(request, result, encoding)
        self.assertEquals("InitialTwoOne", new_result)
        
        published = FauxPublished()
        alsoProvides(published, IPublishedMarker)
        request = FauxRequest(published)
        result = ["Initial"]
        encoding = 'utf-8'
        
        new_result = self.t(request, result, encoding)
        self.assertEquals("InitialTwoOneThree", new_result)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTransformChain))
    return suite
