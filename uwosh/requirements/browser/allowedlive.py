from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from uwosh.requirements import check

class AllowedLive(ViewletBase):

    render = ViewPageTemplateFile('allowedlive.pt')

    def update(self):
        
        self.failed_checks = check.failed()
        
        self.shoulddisplay = len(self.failed_checks) > 0
        