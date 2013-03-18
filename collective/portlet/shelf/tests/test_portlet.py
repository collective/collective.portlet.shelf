from zope.component import getUtility, getMultiAdapter
from zope.component import queryMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from Products.Five import zcml

from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.shelf import portletshelf

import collective.portlet.shelf
from collective.portlet.shelf.tests.base import TestCase


class TestPortlet(TestCase):

    def test_adapters(self):
        zcml.load_config('tests/testing.zcml', collective.portlet.shelf)

        # test default view
        document = getattr(self.folder, 'test_document')
        widget = queryMultiAdapter((document, self.app.REQUEST),
                                   name="portlet_shelf_item_view")
        self.failUnless('Default view' in widget(), document)

        # test image view
        image = getattr(self.folder, 'test_image')
        widget = queryMultiAdapter((image, self.app.REQUEST),
                                   name="portlet_shelf_item_view")
        self.failUnless('Image view' in widget(), image)

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.shelf.PortletShelf')
        self.assertEquals(portlet.addview,
                          'collective.portlet.shelf.PortletShelf')

    def test_interfaces(self):
        portlet = portletshelf.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.shelf.PortletShelf')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={'header': 'shelf',
                                   'target_collection': 'collection'})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   portletshelf.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = portletshelf.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, portletshelf.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)
        assignment = portletshelf.Assignment()
        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, portletshelf.Renderer))


class TestRenderer(TestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        assignment = assignment or portletshelf.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render(self):
        # zcml.load_config('tests/testing.zcml', collective.portlet.shelf)
        r = self.renderer(context=self.portal,
                          assignment=portletshelf.Assignment(header='shelf',
                          target_collection='/'.join(self.folder.collection.getPhysicalPath()[2:])))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.failUnless('test_document' in output,
                        "Default view content is missing in portlet renderer output.")
        self.failUnless('test_image' in output,
                        "Image view content is missing in portlet renderer output.")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    # suite.addTest(makeSuite(TestRenderer))
    return suite
