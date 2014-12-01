from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from uwosh.core.utils import *
from zope.i18nmessageid import MessageFactory
mf = MessageFactory('uwosh.requirements')

def getProperties():
    return retrieve('uwosh_requirements_properties').properties