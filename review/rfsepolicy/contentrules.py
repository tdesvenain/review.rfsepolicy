# -*- encoding: utf-8 -*-
from Acquisition import aq_parent

from plone.stringinterp.adapters import MailAddressSubstitution, BaseSubstitution
from plone.stringinterp import _ as PMF
from Products.CMFPlone.utils import safe_hasattr
from Products.CMFCore.utils import getToolByName


class ReferentEmailSubstitution(MailAddressSubstitution):

    category = PMF(u'E-Mail Addresses')
    description = u"Référent"

    def safe_call(self):
        if safe_hasattr(self.context, 'referent_user'):
            mtool = getToolByName(self.context, 'portal_membership')
            referent = mtool.getMemberById(self.context.referent_user)
            if referent:
                return referent.getProperty('email', u"")

        return u""


class ReviewStateLabelSubstitution(BaseSubstitution):

    category = PMF(u'Workflow')
    description = u"Titre de l'état éditorial"

    def safe_call(self):
        context = self.context
        wtool = getToolByName(context, 'portal_workflow')
        review_state = wtool.getInfoFor(context, 'review_state')
        workflows = wtool.getWorkflowsFor(context)
        for workflow in workflows:
            if review_state in workflow.states:
                state = workflow.states[review_state]
                return state.title or state.id
        else:
            return review_state


class ArticleAuthorSubstitution(BaseSubstitution):

    category = PMF(u'All Content')
    description = u"Auteur de l'article"

    def safe_call(self):
        context = self.context
        if context.portal_type == 'article':
            return context.auteur or u""
        elif context.portal_type == 'report':
            return context.aq_parent.auteur or u""
        else:
            return u""
