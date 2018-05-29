# -*- encoding: utf-8 -*-
from datetime import datetime
from StringIO import StringIO

import xlwt as xl
from xlwt import CompoundDoc

from DateTime import DateTime
from zope.schema import getFieldsInOrder

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from plone.namedfile.file import NamedBlobFile


titlestyle = xl.easyxf('font: height 300, name Times New Roman, colour_index black, bold on, italic off; '
                        'align: wrap on, vert center, horiz center; '
                        'borders: top thin, bottom thin, left thin, right thin; '
                        'pattern: pattern solid, back_colour white, fore_colour white'
                           )

headerstyle = xl.easyxf('font: height 250, name Times New Roman, colour_index black, bold off, italic on; '
                        'align: wrap on, vert top, horiz center; '
                        'borders: top thin, bottom thin, left thin, right thin; '
                        'pattern: pattern solid, back_colour white, fore_colour white'
                           )

titlecellstyle = xl.easyxf('font: height 200, name Times New Roman, colour_index black, bold off, italic on; '
                        'align: wrap on, vert top, horiz center; '
                        'borders: top thin, bottom thin, left thin, right thin; '
                        'pattern: pattern solid, back_colour white, fore_colour white'
                           )
numcellstyle = xl.easyxf('font: height 250, name Times New Roman, colour_index black, bold off; '
                         'align: wrap on, vert bottom, horiz right;'
                         'pattern: pattern solid, back_colour gray25, fore_colour gray25'
                         )

cellstyle = xl.easyxf('font: height 250, name Times New Roman, colour_index black, bold off; '
                     'align: wrap on, vert top, horiz center;'
                     'borders: top thin, bottom thin, left thin, right thin;'
                     'pattern: pattern solid, back_colour white, fore_colour white'
                     )

remarques_cellstyle = xl.easyxf('font: height 250, name Times New Roman, colour_index black, bold off; '
                     'align: wrap on, vert top, horiz left;'
                     'borders: top thin, bottom thin, left thin, right thin;'
                     'pattern: pattern solid, back_colour white, fore_colour white'
                     )


row_height = 1800

ignored = ('file', 'remarques')

class ExcelExport(BrowserView):

    def get_filename(self):
        date = DateTime().strftime('%Y-%m-%d')
        return '%s-%s-.xls' % (self.context.getId(), date)

    def get_schema(self):
        ttool = getToolByName(self.context, 'portal_types')
        article = ttool.article
        return article.lookupSchema()

    def __call__(self):
        wtool = getToolByName(self.context, 'portal_workflow')
        self.request.response.setHeader(
            'Content-type', 'application/vnd.ms-excel;charset=windows-1252')
        self.request.response.setHeader(
            'Content-disposition',
            'attachment; filename="%s"' % self.get_filename()
            )

        # creation du doc
        buffer = StringIO()
        xlDoc = xl.Workbook(encoding='utf-8')

        # initialise la feuille
        sheet = xlDoc.add_sheet('Articles')
        sheet.col(0).width = 256 * 5
        sheet.col(1).width = 256 * 40
        sheet.col(2).width = 256 * 25
        sheet.col(3).width = 256 * 50
        sheet.col(4).width = 256 * 20
        sheet.col(5).width = 256 * 20
        sheet.col(6).width = 256 * 20
        headerline = 3

        # schema de l'article
        schema = self.get_schema()

        # case de titre
        sheet.row(1).height = 1200
        sheet.write_merge(1, 1, 1, 5,
                          "Revue Française de Socio-Economie -%s" % self.context.Title(),
                          titlestyle)

        # ligne de titres
        sheet.write(headerline, 0, "", numcellstyle)
        sheet.write(headerline, 1, u"Titre", headerstyle)
        sheet.write(headerline, 2, u"État", headerstyle)
        fields = [(name, field)
                  for name, field in getFieldsInOrder(schema)
                  if name in ('auteur', 'date_de_r_ception', 'referent_user', 'thema')]
        for num, fieldinfo in enumerate(fields):
            name, field = fieldinfo
            sheet.write(headerline, num+3, field.title, headerstyle)

        sheet.row(headerline).height = row_height

        # lignes de valeurs
        for numart, obj in enumerate(self.get_contents()):
            row = 2 * numart + headerline + 1

            sheet.row(row).height = row_height

            # article number
            sheet.write(row, 0, str(numart), numcellstyle)

            # title
            sheet.write_merge(row, row + 1, 1, 1, obj.Title(), titlecellstyle)

            # état
            review_state = wtool.getInfoFor(obj, 'review_state')
            state = wtool.getTitleForStateOnType(review_state, 'article')
            sheet.write(row, 2, state, cellstyle)

            # dynamic fields
            sheet.row(row).height = 350
            for num, fieldinfo in enumerate(fields):
                name, field = fieldinfo
                value = getattr(obj, name, "")

                if isinstance(value, datetime):
                    value = value.strftime('%d/%m/%Y')

                if not value:
                    value = ""

                if type(value) == unicode:
                    cellvalue = value.encode('utf-8')
                elif type(value) == NamedBlobFile:
                    cellvalue = value.filename.encode('utf-8')
                else:
                    cellvalue = str(value)

                sheet.write(row, num + 3, cellvalue, cellstyle)
                # if obj.remarques:
                # else:
                    #sheet.write_merge(row, row + 1, num + 3, num + 4, cellvalue, cellstyle)

            # ligne de remarques
            remarques = u""
            if obj.evaluateur_1:
                remarques += u"Évaluateur 1: %s - envoi: %s - evaluation: %s - réponse: %s\n" % (
                    obj.evaluateur_1,
                    obj.dateenvoi_1 and obj.dateenvoi_1.strftime('%d/%m/%Y') or u"?",
                    obj.date_evaluation_evaluateur_1 and obj.date_evaluation_evaluateur_1.strftime('%d/%m/%Y') or u"?",
                    obj.reponse_1 or u"?")

            if obj.evaluateur_2:
                remarques += u"Évaluateur 2: %s - envoi: %s - evaluation: %s - réponse: %s\n" % (
                    obj.evaluateur_2,
                    obj.dateenvoi_2 and obj.dateenvoi_2.strftime('%d/%m/%Y') or "?",
                    obj.date_evaluation_evaluateur_2 and obj.date_evaluation_evaluateur_2.strftime('%d/%m/%Y') or "?",
                    obj.reponse_2 or u"?")

            if obj.evaluateur_3:
                remarques += u"Évaluateur 3: %s - envoi: %s - evaluation: %s - réponse: %s\n" % (
                    obj.evaluateur_3,
                    obj.dateenvoi_3 and obj.dateenvoi_3.strftime('%d/%m/%Y') or "?",
                    obj.date_evaluation_evaluateur_3 and obj.date_evaluation_evaluateur_3.strftime('%d/%m/%Y') or "?",
                    obj.reponse_3 or u"?")

            remarques += obj.remarques or u""
            sheet.write_merge(row + 1, row + 1, 2, len(fields) + 2, remarques, remarques_cellstyle)
            sheet.row(row + 1).height = len(remarques.split('\n')) * 350 if remarques else 0


        # enregistre le fichier
        doc = CompoundDoc.XlsDoc()
        data = xlDoc.get_biff_data()
        doc.save(buffer, data)

        return buffer.getvalue()


class TopicExcelExport(ExcelExport):

    def get_contents(self):
        return self.context.queryCatalog(full_objects=True)


class FolderExcelExport(ExcelExport):

    def get_contents(self):
        return self.context.getFolderContents(full_objects=True)


class ExportButton(ViewletBase):


    def render(self):
        return """
                <a id="excel-export"
                   class="visualNoPrint"
                   title="Export Excel"
                   href="%(url)s/excelexport.xls">
                    <img width="16" height="16" title="Export excel" alt="Export excel"
                         src="%(portal_url)s/xls.png">
                <span>Export excel de "%(title)s"</span></a>
               """ % {'title': self.context.Title().decode('utf-8'),
                      'url': self.context.absolute_url(),
                      'portal_url': self.site_url}

