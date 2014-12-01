from zope.interface import Interface, Attribute
from zope import schema

from plone.theme.interfaces import IDefaultPloneLayer

class IUWOshRequirementsLayer(Interface):
    """Marker interface that defines a browser layer
    """


class IGoLiveCheck(Interface):
    
    name = Attribute("The name of the check")
    description = Attribute("articulated description of the check")
    fixinginfo = Attribute("information on how to fix the problem")
    
    def passes(self):
        """
        returns boolean on if it passes
        """
        
    def use(self):
        """
        defines if the check should be used or not
        """