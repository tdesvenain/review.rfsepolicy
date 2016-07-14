from plone.dexterity.interfaces import IDexterityContainer
from plone.indexer.decorator import indexer

@indexer(IDexterityContainer)
def searchable(obj):
    searchable_text = obj.SearchableText()
    if obj.portal_type == 'article':
        if obj.auteur:
            searchable_text += u" " + obj.auteur

    return searchable_text
