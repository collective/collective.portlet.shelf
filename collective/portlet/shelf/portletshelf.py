from zope.interface import implements

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
    page_size = schema.Int(
        title=_(u"Number of items"),
        description=_(u"Enter the number of content items to be displayed."),
        default=1,
        required=True)

    height = schema.Int(
        title=_(u"Page Height"),
        description=_(u"Specify the height of portlet in pixels."),
        default=200,
        required=True)

    width = schema.Int(
        title=_(u"Page Width"),
        description=_(u"Specify the width of portlet in pixels."),
        default=160,
        required=True)


class Assignment(base.Assignment):
    """Portlet shelf assignment.

    """
    implements(IPortletShelf)

    show_more = False
    page_size = 1
    height = 200
    width = 160

    def __init__(self, header=u"", target_collection=None, limit=0,
                 random=False, show_more=False, show_dates=False, page_size=1,
                 height=200, width=160):
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.random = random
        self.show_more = show_more
        self.show_dates = show_dates
        self.page_size = page_size
        self.height = height
        self.width = width

    @property
    def title(self):
        return self.header or _(u"Portlet Shelf")


class Renderer(base.Renderer):
    """Portlet shelf renderer.

    """

    render = ViewPageTemplateFile('portletshelf.pt')

    def sub_topics(self):
        """Returns list of subtopic objects.

        """
        catalog = getToolByName(self.context, 'portal_catalog')
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
        collections = [{'id': topic.getId(),
                        'title': topic.Title(),
                        'content': topic.queryCatalog()}
                       for topic in self.sub_topics() if topic.queryCatalog()]

        # add main collection
        collections.append({'id': 'main',
                            'title': _('All'),
                            'content': self.results()})
        return collections

    def height_and_width_style(self):
        return "height:%spx;width:%spx;" % (self.data.height, self.data.width)

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
    form_fields = form_fields.omit('show_dates')

    label = _(u"Add Shelf Portlet")
    description = _(
        u"This portlet display a scrollable items from Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet shelf edit form.
"""
    form_fields = form.Fields(IPortletShelf)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields = form_fields.omit('show_dates')

    label = _(u"Edit Shelf Portlet")
    description = _(
        u"This portlet display a scrollable items from Collection.")
