from zope.interface import implements, Interface
from zope.component import adapts

from collective.edm.listing.listingrights import DefaultListingRights
from collective.edm.listing.listingoptions import DefaultListingOptions
from collective.edm.listing.interfaces import IEDMListingSupplColumn,\
    IEDMListing
from review.rfsepolicy.interfaces import IRFSELayer
from Products.CMFCore.interfaces import IFolderish


class RFSEListingRights(DefaultListingRights):
    adapts(IFolderish, IRFSELayer, IEDMListing)

    _external_editable_types = ()

    def globally_show_state(self, brains):
        """View state column
        """
        for brain in brains:
            if brain.review_state and brain.review_state != 'published':
                return True
        else:
            return False

    def globally_show_sort(self):
        """View sort column
        """
        return False

    def globally_can_copy(self, brains):
        """View copy column
        """
        return False

    def globally_can_cut(self, brains):
        """View cut column
        """
        return False

    def globally_show_author(self):
        """View cut column
        """
        return False

    def globally_show_download(self, brain):
        """View state column
        """
        return False


class RFSEListingOptions(DefaultListingOptions):
    adapts(IFolderish, IRFSELayer, IEDMListing)

    sort_mode = 'auto'
    default_sort_on = 'modified'
    default_sort_order = 'descending'
    allow_edit_popup = True


class AuthorColumn(object):
    implements(IEDMListingSupplColumn)
    adapts(IFolderish, IRFSELayer, Interface, IEDMListing)

    def __init__(self, context, request, table, view):
        pass

    header = "Auteur"

    def value(self, item):
        return item['brain'].auteur

