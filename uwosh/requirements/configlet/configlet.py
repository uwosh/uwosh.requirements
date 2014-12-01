from plone.memoize.instance import memoize

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility
from uwosh.requirements.golivechecks import CheckMustClickReadyToGoLive
from zope.app.component.hooks import getSite
from zope.component import getMultiAdapter
from uwosh.requirements.utils import getProperties
from zLOG import LOG, WARNING
from uwosh.requirements import check

class UWOshRequirementsConfiglet(BrowserView):
    """Manage rules in a the global rules container
    """
    
    template = ViewPageTemplateFile('uwosh-requirements.pt')
    errormsg = ""

    def __call__(self):
        form = self.request.form
        btn = form.get('form.button.GoLive', None)
        url = form.get('form.plone-projects-url', None)
        
        if url is not None and len(url) == 0:
            self.errormsg = 'Must enter plone project url'
        elif btn is not None and url is not None:
            self.goLive(url)
            
        return self.template()
        
    @memoize
    def checks(self):
        return check.get_all()
        
    @memoize
    def requirements_met(self):        
        def or_test(check):
            if check.__class__ == CheckMustClickReadyToGoLive:
                return True
                
            return False
        
        return check.all_requirements_met(or_test=or_test)
        
    @memoize
    def is_live(self):
        site = getSite()
        
        viewlet = "uwosh.allowedlive"
        manager = "plone.portaltop"

        storage = getUtility(IViewletSettingsStorage)
        skinname = site.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)

        return viewlet in hidden
        
    def goLive(self, url):
        
        if self.requirements_met() and not self.is_live():
        
            site = getSite()
            viewlet = "uwosh.allowedlive"
            manager = "plone.portaltop"

            storage = getUtility(IViewletSettingsStorage)
            skinname = site.getCurrentSkinName()
            hidden = storage.getHidden(manager, skinname)

            if viewlet not in hidden:
                hidden = hidden + (viewlet,)
                storage.setHidden(manager, skinname, hidden)
        
            message = """
The site '%s' is ready to go live.
The plone project url is %s
Administrators on this site are: 
            """ % (site.Title(), url)
            
            administrators = site.portal_groups.getGroupMembers('Administrators')
            for admin in administrators:
                admin_obj = site.portal_membership.getMemberById(admin)
                message = message + """
%s
---------------
User Id: %s
Email: %s
                """ % (admin_obj.getProperty('fullname', None), admin, admin_obj.getProperty('email', None))
            
            mTo = getProperties().golive_email_address
            mFrom = site.email_from_address
            mSubject = "Site '%s' is ready to go live" % site.Title()
            
            site.MailHost.secureSend(message, mTo, mFrom, mSubject)
            
            url = getMultiAdapter((self.context, self.request), name='absolute_url')()
            self.request.response.redirect(url + '/@@uwosh-requirements')
            
            
        
        