import binascii
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.app.container.interfaces import INameChooser
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from zope import schema
from zope.formlib import form
from zope.component import queryMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.portlet.collection import collection as base
from collective.portlet.shelf import PortletShelfMessageFactory as _
from plone.memoize.instance import memoize


class IPortletShelf(base.ICollectionPortlet):
    """A marker interface for scrollable plone
    portlet that based on plone collection portlet.

    """

class Assignment(base.Assignment):
    """Portlet shelf assignment.

    """
    implements(IPortletShelf)

    @property
    def title(self):
        return self.header or u"Portlet Shelf"


class Renderer(base.Renderer):
    """Portlet shelf renderer.

    """

    render = ViewPageTemplateFile('portletshelf.pt')
    
    def sub_topics(self):
        """Returns list of subtopic objects.

        """
        catalog  = getToolByName(self.context, 'portal_catalog')
        curl = self.data.collection().absolute_url()
        brains = catalog(path='/'.join(self.collection().getPhysicalPath()),
                         portal_type='Topic')
        return [br.getObject() for br in brains if br.getURL() != curl]
    
    @memoize
    def collections(self):
        """
        Returns all collection content
        with subcollections.
        
        """
        collections = [{'id':topic.getId(),
                        'title':topic.Title(),
                        'content':topic.queryCatalog()}
                        for topic in self.sub_topics() if topic.queryCatalog()]

        #add main collection
        collections.append({'id':'main',
                            'title':'All',
                            'content':self.results()})

        return collections

    def widget(self, item):
        widget = queryMultiAdapter((item.getObject(), self.request),
                                   name="portlet_shelf_item_view")
        if widget is not None:
            return widget()

class AddForm(base.AddForm):
    """Portlet shelf add form.

    """
    form_fields = form.Fields(IPortletShelf)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields = form_fields.omit('random', 'show_more', 'show_dates')

    label = _(u"Add Shelf Portlet")
    description = _(u"This portlet display a scrollable items from Collection.")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet shelf edit form.
"""
    form_fields = form.Fields(IPortletShelf)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields = form_fields.omit('random', 'show_more', 'show_dates')

    label = _(u"Edit Shelf Portlet")
    description = _(u"This portlet display a scrollable items from Collection.")
