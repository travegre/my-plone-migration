# coding=utf-8
"""Definition of the dezurstvo content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from nadomescanja.produkti.interfaces import Idezurstvo
from nadomescanja.produkti.config import PROJECTNAME

from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import *

from Products.CMFCore.exceptions import BadRequest
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import *
from Products.CMFCore import permissions as CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.CMFCore.utils import getToolByName
import os
from zipfile import ZipFile
import mimetypes
from StringIO import StringIO
import base64
import cStringIO
import xlrd
import openpyxl
import sys
import random
import DateTime
import json



dezurstvoSchema = folder.ATFolderSchema.copy() + atapi.Schema((

  
    atapi.TextField(
        'nadomescanja_json',
        required=False,
        default='[]',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=u"Nadomeščanja (JSON)",
            visible={'view': 'visible', 'edit': 'hidden'},  # hidden
        ),
    )

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

dezurstvoSchema['title'].storage = atapi.AnnotationStorage()
dezurstvoSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    dezurstvoSchema,
    folderish=True,
    moveDiscussion=False
)


class dezurstvo(folder.ATFolder):
    add_permission = CMFCorePermissions.AddPortalContent

    """Description of the Example Type"""
    implements(Idezurstvo)

    meta_type = "dezurstvo"
    schema = dezurstvoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    nadomescanja_json = atapi.ATFieldProperty('nadomescanja_json')

    def getNadomescanjaRows(self):        
        try:    return json.loads(self.getNadomescanja_json() or '[]')
        except: return []

    def getNadomescanjaDict(self):
        """Convert nadomescanje rows to dict."""
        nadomescanja = {}
        rows = self.getNadomescanjaRows()
        for row in rows:
            nadomescanja[row['laboratorij_okrajsava']] = row['nadomestni_vodja_naziv'] 
        
        return nadomescanja

    # this is used in the spremeni dezurstvo form
    def getSampleVocabulary50(self):
        obj = self.portal.restrictedTraverse('dezurstva/seznam_zaposlenih')
        obj = obj.getFolderContents(contentFilter={'sort_on':'getObjPositionInParent'})             
                                 
        xx = [('','')]
        for x in obj:
            if '|' in str(x.Description) and not x.getObject().getExcludeFromNav():
                xx.append((str(x.Description).split('|')[1] == '-' and x.id or str(x.Description).split('|')[1], x.Title.decode('utf-8')))
        
        return xx

    security = ClassSecurityInfo()

    def excel_export(self, first_day, last_day, oseba):
    
        nadomescanja = self.portal_catalog(portal_type = "dezurstvo", sort_on="id")
        nadomescanja = [x for x in nadomescanja if 'undefined' not in x.id and x.id != 'objekt-za-seznam-zaposlenih-v-formi-spremeni-nadomescanje-ne-brisi' and DateTime.DateTime(x.id) >= first_day and DateTime.DateTime(x.id) <= last_day]

        if oseba:            
            nadomescanja_oseba = []
            for x in nadomescanja:
                lista = x.getObject().getNadomescanjaRows()
                for h in lista:
                    if oseba == h['nadomestni_vodja_id']:
                        nadomescanja_oseba.append(x)
            nadomescanja = set(nadomescanja_oseba)

        # create excel
        workBookDocument = openpyxl.Workbook()
        docSheet1 = workBookDocument.add_sheet('izpis')
        
        od = first_day.Date()
        od = '.'.join([od.split('/')[2], od.split('/')[1], od.split('/')[0]])
        do = last_day.Date()
        do = '.'.join([do.split('/')[2], do.split('/')[1], do.split('/')[0]])
        
        if oseba:
            person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + oseba).Title().decode('utf-8')
            docSheet1.write(0, 0, 'Izpis: ' + od + ' - ' + do + ' za osebo ' + person)
        else:
            docSheet1.write(0, 0, 'Izpis: ' + od + ' - ' + do)

        count = 2

        docSheet1.write(count, 0, 'Datum')
        docSheet1.write(count, 1, 'Enota')
        docSheet1.write(count, 2, 'Vodja')
        docSheet1.write(count, 3, u'Nadomešča')

        for j, i in enumerate(nadomescanja):
            count += 1
            datum = '.'.join([i.id.split('-')[2], i.id.split('-')[1], i.id.split('-')[0]])            
            lista = i.getObject().getNadomescanjaRows()
            
            for h in lista:
                if not oseba or (oseba and oseba == h['nadomestni_vodja_id']): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, h['laboratorij_okrajsava'])
                    docSheet1.write(count, 2, h['privzeti_vodja_naziv'])
                    docSheet1.write(count, 3, h['nadomestni_vodja_naziv'])

        dat = StringIO()
        workBookDocument.save(dat)

        # output zip file
        r = self.portal.REQUEST  
        r.RESPONSE.setHeader("Content-type","application/vnd.ms-excel")        
        od = first_day.Date()
        od = '_'.join([od.split('/')[2], od.split('/')[1], od.split('/')[0]])
        do = last_day.Date()
        do = '_'.join([do.split('/')[2], do.split('/')[1], do.split('/')[0]])
        filename = 'izpis_' + od + '-' + do + '.xls'
        r.RESPONSE.setHeader("Content-disposition","attachment;filename=" + filename)    
        r.RESPONSE.write(dat.getvalue())
        
        return r.RESPONSE

atapi.registerType(dezurstvo, PROJECTNAME)
