from interfaces import IGoLiveCheck
from zope.app.component.hooks import getSite
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.interface import implements
from zope.component import getUtility
from Products.Five.testbrowser import Browser
from Products.CMFCore.utils import getToolByName
from uwosh.core.utils import *

CHECKS = []

def registerCheck(check):
    
    if check not in CHECKS:
        CHECKS.append(check)

class CheckEmail:
    
    implements(IGoLiveCheck)
    
    name = "Email"
    description = "Must set site from address in Mail Settings"
    fixinginfo = """Go to <a href="@@mail-controlpanel">Mail Settings</a> and set the required information"""
    
    def use(self):
        """
        always use
        """
        return True
    
    def passes(self):
        site = getSite()
        
        from_address = site.email_from_address
        
        return len(from_address) > 0
        
registerCheck(CheckEmail)

class CheckShouldShowUWBanner:
    implements(IGoLiveCheck)
    
    name = "Show Banner"
    description = "Must show UW Oshkosh Banner"
    fixinginfo = """ Go to <a href="@@uwosh.theme.configuration">uwosh theme configuration</a> and show the banner """
    
    def use(self):
        return has.product("uwosh.themebase").installed()
    
    def passes(self):
                    
        site = getSite()
        
        viewlet = "uwosh.theme.base.banner"
        manager = "plone.portaltop"

        storage = getUtility(IViewletSettingsStorage)
        skinname = site.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)

        return viewlet not in hidden

#registerCheck(CheckShouldShowUWBanner)

class CheckShouldShowSearchBox:
    implements(IGoLiveCheck)
    
    name = "Show Search Box"
    description = "Must show search box"
    fixinginfo = """ Go to <a href="@@manage-viewlets">manage viewlets</a> and show the search box """
    
    def use(self):
        return True
    
    def passes(self):
        site = getSite()
        
        viewlet = "plone.searchbox"
        manager = "plone.portalheader"

        storage = getUtility(IViewletSettingsStorage)
        skinname = site.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)

        return viewlet not in hidden

#depreciated since the search is now in the banner viewlet
#registerCheck(CheckShouldShowSearchBox)

class CheckShouldShowUWOshFooter:
    implements(IGoLiveCheck)
    
    name = "Show UWOsh Footer"
    description = "Must show UW Oshkosh footer"
    fixinginfo = """ Go to <a href="@@manage-viewlets">manage viewlets</a> and show the uwosh.theme.base.footer viewlet """
    
    def use(self):
        return has.product("uwosh.themebase").installed()
    
    def passes(self):
        site = getSite()
        
        viewlet = "uwosh.theme.base.footer"
        manager = "plone.portalfooter"

        storage = getUtility(IViewletSettingsStorage)
        skinname = site.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)

        return viewlet not in hidden

#registerCheck(CheckShouldShowUWOshFooter)

class CheckNeedsClickableLinkInFooter:
    implements(IGoLiveCheck)
    
    name = "Clickable Link In Footer"
    description = "Must have clickable link in footer"
    fixinginfo = """ Go to <a href="@@uwosh.theme.configuration">uwosh theme configuration</a> and add link to uwosh.edu in the footer """
    
    def use(self):
        return has.product("uwosh.theme").installed()
    
    def passes(self):
        site = getSite()
        
        #in case uwosh theme isn't installed
        props = retrieve('uwosh_theme_properties').properties
        footer = None
        if props:
            footer = props.footer

        if not footer or len(footer) == 0:
            return False

        if footer.find('href=') >= 0 and footer.find('uwosh.edu') >= 0:
            return True
        else:
            return False

#depreciated since there is no longer needed a link in the footer
#registerCheck(CheckNeedsClickableLinkInFooter)

class CheckNeedsSiteMapAccessiblityAndContactLinks:
    implements(IGoLiveCheck)
    
    name = "Missing Required Links"
    description = "Must show site map, accessiblity, and contact links on page"
    fixinginfo = """ Go to <a href="manage">ZMI</a> and the links back in portal_actions """
    
    def use(self):
        return True
    
    def passes(self):
        site = getSite()
        atool = getToolByName(site, 'portal_actions')
        actions = atool.listFilteredActionsFor(site)['site_actions']
        
        foundSiteMap = False
        foundAccessiblity = False
        foundContact = False
        
        for action in actions:
            if action['title'] == u"Site Map" and action['visible']:
                foundSiteMap = True
            elif action['title'] == u'Accessibility' and action['visible']:
                foundAccessibility = True
            elif action['title'] == u'Contact' and action['visible']:
                foundContact = True
            
        return foundSiteMap and foundAccessibility and foundContact

registerCheck(CheckNeedsSiteMapAccessiblityAndContactLinks)

class CheckViewAbout:
    implements(IGoLiveCheck)
    
    name = "View About"
    description = "Anyone must be allowed to view about information"
    fixinginfo = """ Go to <a href="@@security-controlpanel">security settings</a> and check "Allow anyone to view 'about' information" """
    
    def use(self):
        return True
    
    def passes(self):
        site = getSite()
        pprops = getToolByName(site, 'portal_properties')
        
        return pprops.site_properties.allowAnonymousViewAbout

registerCheck(CheckViewAbout)

class CheckExposeSiteMap:
    implements(IGoLiveCheck)
    
    name = "Expose sitemap.xml.gz"
    description = "Must expose site map"
    fixinginfo = """ Go to <a href="@@site-controlpanel">site settings</a> and check "Expose sitemap.xml.gz in the portal root" """
    
    def use(self):
        return True
    
    def passes(self):
        site = getSite()
        pprops = getToolByName(site, 'portal_properties')
        
        return pprops.site_properties.enable_sitemap

registerCheck(CheckExposeSiteMap)

class CheckSiteDescription:
    implements(IGoLiveCheck)
    
    name = "Site Description"
    description = "Must have a site description"
    fixinginfo = """ Go to <a href="@@site-controlpanel">site settings</a> and fill in a site description """
    
    def use(self):
        return True
    
    def passes(self):
        site = getSite()
        return len(site.description) > 0

registerCheck(CheckSiteDescription)

class CheckCSSDebugging:
    implements(IGoLiveCheck)

    name = "CSS Debugging"
    description = "Must have CSS debugging turned off"
    fixinginfo = """ Go to <a href="manage">ZMI</a> -> portal_css and uncheck "Debug/development mode" """

    def use(self):
        return True

    def passes(self):
        site = getSite()
        pcss = getToolByName(site, 'portal_css')
        return not pcss.getDebugMode()

registerCheck(CheckCSSDebugging)

class CheckJSDebugging:
    implements(IGoLiveCheck)

    name = "JS Debugging"
    description = "Must have JS debugging turned off"
    fixinginfo = """ Go to <a href="manage">ZMI</a> -> portal_javascripts and uncheck "Debug/development mode" """

    def use(self):
        return True

    def passes(self):
        site = getSite()
        pjs = getToolByName(site, 'portal_javascripts')
        return not pjs.getDebugMode()

registerCheck(CheckJSDebugging)

class CheckCacheSetupInstalled:
    implements(IGoLiveCheck)

    name = "CacheSetup Installed"
    description = "Must have CacheSetup installed"
    fixinginfo = """ Go to <a href="prefs_install_products_form">Add-On Products</a> -> install CacheSetup """

    def use(self):
        return True

    def passes(self):
        site = getSite()
        pq = getToolByName(site, 'portal_quickinstaller')
        return pq.isProductInstalled("CacheSetup")

registerCheck(CheckCacheSetupInstalled)

class CheckCacheFuEnabled:
    implements(IGoLiveCheck)

    name = "CacheFu Enabled"
    description = "Must have CacheFu enabled"
    fixinginfo = """ Go to the <a href="portal_cache_settings">Cache Configuration Tool</a> -> and check "Enable CacheFu" """
    


    def use(self):
        site = getSite()
        pq = getToolByName(site, 'portal_quickinstaller')
        return pq.isProductInstalled("CacheSetup")

    def passes(self):
        site = getSite()
        pcs = getToolByName(site, 'portal_cache_settings')
        return pcs.getEnabled()

registerCheck(CheckCacheFuEnabled)

class CheckNotLetUsersSelectOwnPasswords:
    implements(IGoLiveCheck)

    name = "Let Users Select Passwords"
    description = "Must not let users select their own password"
    fixinginfo = """ Go to <a href="@@security-controlpanel">site security</a> and uncheck the box labled "Let users select their own passwords" """

    def use(self):
        return True

    def passes(self):
        site = getSite()

        return site.validate_email

registerCheck(CheckNotLetUsersSelectOwnPasswords)

class CheckMailHostMustBeSet:
    implements(IGoLiveCheck)

    name = "Mail Server"
    description = "Mail Server host must be set to smtp.uwosh.edu"
    fixinginfo = """ Go to <a href="@@mail-controlpanel">mail settings</a> enter "smtp.uwosh.edu" as the mail host. """

    def use(self):
        return True

    def passes(self):
        site = getSite()

        return site.MailHost.smtp_host == "smtp.uwosh.edu"

registerCheck(CheckMailHostMustBeSet)

class CheckLoginFormInCustom:
    implements(IGoLiveCheck)
    
    name = "Use Campus Login Form"
    description = "Must use the campus login form"
    fixinginfo = """ Go to <a href="manage/portal_skins/custom">the custom folder</a> and delete login_form """
    
    def use(self):
        return has.product("uwosh.themebase").installed()
    
    def passes(self):   
        site = getSite()
        ps = getToolByName(site, 'portal_skins')
        custom = ps['custom']
        return 'login_form' not in custom.objectIds()

registerCheck(CheckLoginFormInCustom)

class CheckMustClickReadyToGoLive:
    implements(IGoLiveCheck)

    name = "Go Live"
    description = "Notify uwosh staff you are ready to go live"
    fixinginfo = """ Go to <a href="@@uwosh-requirements">uwosh requirements</a>, enter the plone project url and click "ready to go live" """

    def use(self):
        return True

    def passes(self):
        site = getSite()

        viewlet = "uwosh.allowedlive"
        manager = "plone.portaltop"

        storage = getUtility(IViewletSettingsStorage)
        skinname = site.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)

        return viewlet in hidden

registerCheck(CheckMustClickReadyToGoLive)
