from zope.interface import Interface
from zope import schema

class ITransform(Interface):
    """Register a named multi adapter from (published, request,) to
    this interface to change the response.
    
    `published` is the published object, i.e. the last thing being traversed
    to. Typically, it will be a view.
    
    `request` is the request type.
    
    To control the order of transforms, use the 'order' attribute. It may be
    positive or negative.
    """
    
    order = schema.Int(title=u"Order")
    
    def __call__(result, encoding):
        """Modify the result.
        
        `result` is an iterable that represents the response body. When
        unwound, its contents will match the response content type.
        
        `encoding` is the default encoding used.
        
        Return the new result iterable, or a string. If a string is returned,
        the Content-Type header will be updated automatically. If a unicode
        string is returned, it will be encoded with the current content
        encoding.
        
        Return None to indicate that the current value should be changed.
        
        Do not call `request.response.setBody()`. It will have no effect.
        """
