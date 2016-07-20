from plone.dexterity.interfaces import IDexterityContainer
from plone.indexer.decorator import indexer

@indexer(IDexterityContainer)
def searchable(obj):
    searchable_text = obj.SearchableText()
    if obj.portal_type == 'article':
        if obj.auteur:
            searchable_text += " "
            searchable_text += obj.auteur.encode('utf-8')

    return searchable_text
