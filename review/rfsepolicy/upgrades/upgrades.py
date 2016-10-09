from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from review.rfsepolicy import logger
from Products.CMFPlone.utils import normalizeString
from ecreall.helpers.upgrade.interfaces import IUpgradeTool


def v2(context):
    portal = context.aq_parent
    ctool = getToolByName(portal, 'portal_catalog')
    articles = ctool.unrestrictedSearchResults(portal_type='article')
    vocabulary = getUtility(IVocabularyFactory, 'plone.principalsource.Users')
    values_dict = dict([(normalizeString(unicode(term.title), context=portal),
                         term.value)
                        for term in vocabulary(portal)])

    for article in articles:
        article = article.getObject()
        if not article.referent:
            continue

        referent_name = normalizeString(article.referent, context=portal,
                                        encoding='utf-8')
        if referent_name in values_dict:
            article.referent_user = values_dict[referent_name]
            article.referent = u""
        else:
            logger.info("%s : Couldn't find referent %s",
                        article.absolute_url(), article.referent)

    context.runImportStepFromProfile('profile-review.rfsepolicy:default',
                        'typeinfo', run_dependencies=False, purge_old=False)

    context.runImportStepFromProfile('profile-review.rfsepolicy:default',
                        'catalog', run_dependencies=False, purge_old=False)
    context.runImportStepFromProfile('profile-review.rfsepolicy:default',
                        'portlets', run_dependencies=False, purge_old=False)
    context.runImportStepFromProfile('profile-review.rfsepolicy:default',
                        'contentrules', run_dependencies=False, purge_old=False)
    context.runImportStepFromProfile('profile-review.rfsepolicy:default',
                        'atcttool', run_dependencies=False, purge_old=False)
    portal.portal_quickinstaller.reinstallProducts(['collective.edm.listing'])
    portal.portal_catalog.manage_catalogReindex(portal.REQUEST,
                                                portal.REQUEST.RESPONSE,
                                                portal.REQUEST.URL1)


def v3(context):
    context.runImportStepFromProfile('profile-review.rfsepolicy:default',
                        'jsregistry', run_dependencies=False, purge_old=False)
    IUpgradeTool(context).runImportStep('review.rfsepolicy', 'browserlayer')


def v4(context):
    from plone.namedfile.file import NamedBlobFile
    tool = IUpgradeTool(context)
    tool.uninstallProduct('uwosh.northstar')
    tool.installProduct('plone.app.workflowmanager')
    tool.uninstallProduct('plone.app.versioningbehavior')
    tool.installProduct('plone.app.versioningbehavior')
    tool.runImportStep('review.rfsepolicy', 'typeinfo')
    tool.portal.portal_catalog.manage_catalogReindex(context.REQUEST, context.REQUEST.RESPONSE, '')
    if 'portal_subskinstool' in tool.portal:
        tool.portal.manage_delObjects(['portal_subskinstool'])

    for old_layer in ['collective_cmfeditionsdexteritycompat', 'archetypes_kss', 'plone_kss']:
        if old_layer in tool.portal.portal_skins:
            tool.portal.portal_skins.manage_delObjects([old_layer])

    # todo: remove inline validation

    def migrate_version_1(obj, path):
        if obj.version_1 is not None:
            return
        namedfile = obj.file
        namedblobfile = NamedBlobFile(namedfile.data._data,
                                      contentType=namedfile.contentType,
                                      filename=namedfile.filename)

        obj.version_1 = namedblobfile

    tool.migrateContent('article', migrate_version_1, nofail=True)

    def migrate_report_file(obj, path):
        if obj.file.__class__ is NamedBlobFile:
            return

        namedfile = obj.file
        namedblobfile = NamedBlobFile(namedfile.data._data,
                                      contentType=namedfile.contentType,
                                      filename=namedfile.filename)

        obj.file = namedblobfile

    tool.migrateContent('report', migrate_report_file, nofail=True)


def v5(context):
    tool = IUpgradeTool(context)
    tool.runImportStep('review.rfsepolicy', 'worfklowtool')
    tool.runImportStep('review.rfsepolicy', 'contentrules')
