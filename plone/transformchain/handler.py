from zope.interface import implements
from zope.component import getAdapters

from repoze.zope2.interfaces import ITransformer

from plone.transformchain.interfaces import ITransform

def sort_key(a, b):
    return cmp(a.order, b.order)

class Transformer(object):
    """Delegate the opportunity to transform the response to multiple,
    ordered adapters.
    """
    
    implements(ITransformer)
    
    def __call__(self, request, result, encoding):
    
        published = request.get('PUBLISHED', None)
    
        handlers = [v[1] for v in getAdapters((published, request,), ITransform)]
        handlers.sort(sort_key)
    
        for handler in handlers:
            new_result = handler(result, encoding)
            if new_result is not None:
                result = new_result
    
        return result
