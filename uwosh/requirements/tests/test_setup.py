import unittest
from uwosh.requirements.tests.base import UWOshRequirementsTestCase
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility

class TestSetup(UWOshRequirementsTestCase):
    """
    
    """
    
    def test_actionicon(self):
        ai = getToolByName(self.portal, 'portal_actionicons')
        iconInfo = ai.getActionInfo('controlpanel', 'uwosh.requirements.controlpanel.icon')
        
        self.assertEquals('uwosh control panel icon', iconInfo[0])
        self.assertEquals('product_icon.gif', iconInfo[2])
        
    def test_controlpanel_item_installed(self):
        cp = getToolByName(self.portal, 'portal_controlpanel')
        productsConfiglets = cp.enumConfiglets(group="Products")
        
        #not working...
        #self.failUnless('uwosh.requirements.configlet' in productsConfiglets )

    def test_css_added(self):
        pcss = getToolByName(self.portal, 'portal_css')
        
        self.failUnless('++resource++uwosh.requirements.css' in [css.getId() for css in pcss.getResources()])
        
    def test_viewlet_added(self):
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.portaltop"

        storage = getUtility(IViewletSettingsStorage)
        skinname = self.portal.getCurrentSkinName()
        
        self.failUnless('uwosh.allowedlive' in storage.getOrder(manager, skinname))
        
    def test_viewlet_shown(self):
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.portaltop"

        storage = getUtility(IViewletSettingsStorage)
        skinname = self.portal.getCurrentSkinName()
        
        self.failUnless('uwosh.allowedlive' not in storage.getHidden(manager, skinname))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite