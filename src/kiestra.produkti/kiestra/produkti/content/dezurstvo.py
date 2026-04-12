# coding=utf-8
"""Definition of the dezurstvo content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from kiestra.produkti.interfaces import Idezurstvo
from kiestra.produkti.config import PROJECTNAME

from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import *

from Products.CMFCore.exceptions import BadRequest
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import *

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

import os
from zipfile import ZipFile
import mimetypes
from StringIO import StringIO
import base64
import cStringIO
import xlrd
import xlwt
import sys
import random
import DateTime

dezurstvoSchema = folder.ATFolderSchema.copy() + atapi.Schema((

  
    # -*- Your Archetypes field definitions here ... -*-
    atapi.LinesField(
        'priprava_vzorcev',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label="Priprava vzorcev",
                    
                ),
    ),

    atapi.StringField(
        'priprava_vzorcev_text',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="OPOMBA",                    
                ),
    ),

    atapi.LinesField(
        'cepljenje_vzorcev',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label="Inoqula + Sortera",
                    
                ),
    ),

    atapi.StringField(
        'cepljenje_vzorcev_text',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="OPOMBA",                    
                ),
    ),

    atapi.LinesField(
        'odcitavanje',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label="Odčitavanje",
                    
                ),
    ),

    atapi.StringField(
        'odcitavanje_text',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="OPOMBA",                    
                ),
    ),

    atapi.LinesField(
        'identifikacija',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label="Ime bakterije",
                    
                ),
    ),

    atapi.StringField(
        'identifikacija_text',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="OPOMBA",                    
                ),
    ),

    atapi.LinesField(
        'antibiogram',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label="ID+ATB, ATB, izolacija",
                    
                ),
    ),

    atapi.StringField(
        'antibiogram_text',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="OPOMBA",                    
                ),
    ),

    atapi.LinesField(
        'izolacija',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label="Waste",
                    
                ),
    ),

    atapi.StringField(
        'izolacija_text',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="OPOMBA",                    
                ),
    ),

    atapi.LinesField(
        'odpad',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label="OFF",
                    
                ),
    ),

    atapi.StringField(
        'odpad_text',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="OPOMBA",                    
                ),
    ),

    atapi.LinesField(
        'ciscenje',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label="Čiščenje kiestre",
                    
                ),
    ),

    atapi.StringField(
        'ciscenje_text',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="OPOMBA",                    
                ),
    ),

    atapi.TextField(
        'stalni_tekst',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.TextAreaWidget(
                    label="Stalni tekst",                    
                ),
    ),

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
    """Description of the Example Type"""
    implements(Idezurstvo)

    meta_type = "dezurstvo"
    schema = dezurstvoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    priprava_vzorcev = atapi.ATFieldProperty('priprava_vzorcev')
    cepljenje_vzorcev = atapi.ATFieldProperty('cepljenje_vzorcev')
    odcitavanje = atapi.ATFieldProperty('odcitavanje')
    identifikacija = atapi.ATFieldProperty('identifikacija')
    antibiogram = atapi.ATFieldProperty('antibiogram')
    izolacija = atapi.ATFieldProperty('izolacija')
    odpad = atapi.ATFieldProperty('odpad')
    ciscenje = atapi.ATFieldProperty('ciscenje')

    priprava_vzorcev_text = atapi.ATFieldProperty('priprava_vzorcev_text')
    cepljenje_vzorcev_text = atapi.ATFieldProperty('cepljenje_vzorcev_text')
    odcitavanje_text = atapi.ATFieldProperty('odcitavanje_text')
    identifikacija_text = atapi.ATFieldProperty('identifikacija_text')
    antibiogram_text = atapi.ATFieldProperty('antibiogram_text')
    izolacija_text = atapi.ATFieldProperty('izolacija_text')
    odpad_text = atapi.ATFieldProperty('odpad_text')
    ciscenje_text = atapi.ATFieldProperty('ciscenje_text')

    stalni_tekst = atapi.ATFieldProperty('stalni_tekst')

    def getSampleVocabulary40(self):
                                
        obj = self.portal.restrictedTraverse('dezurstva/seznam_zaposlenih')
        obj = obj.getFolderContents(contentFilter={'sort_on':'getObjPositionInParent'})             
                                 
        xx = []
        for rows in obj:
                if rows.id != "" and not rows.getObject().getExcludeFromNav():
                        xx.append((rows.id, rows.getObject().Title()))
        
        return DisplayList(xx)

    security = ClassSecurityInfo()

atapi.registerType(dezurstvo, PROJECTNAME)
