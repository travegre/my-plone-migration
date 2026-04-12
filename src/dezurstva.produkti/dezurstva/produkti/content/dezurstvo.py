# coding=utf-8
"""Definition of the dezurstvo content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from dezurstva.produkti.interfaces import Idezurstvo
from dezurstva.produkti.config import PROJECTNAME

from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import *

from Products.CMFCore.exceptions import BadRequest
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import *
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

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
from datetime import datetime, timedelta

dezurstvoSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.LinesField(
        'dezurni_zdravnik',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="Dežurni zdravnik",
                    
                ),
    ),

    atapi.LinesField(
        'nadzorni_zdravnik',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="Nadzorni zdravnik",
                    
                ),
    ),

    atapi.LinesField(
        'specializant',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="Specializant na usposabljanju",
                    
                ),
    ),

    atapi.LinesField(
        'sarsifon',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="Virološki laboratoriji",
                    
                ),
    ),    

    atapi.LinesField(
    'dezurni_tehnik',        
    searchable = True,
    storage=atapi.AnnotationStorage(),
    vocabulary="getSampleVocabulary40",        
    widget=atapi.InAndOutWidget(
                visible = {'view' : 'invisible', 
               'edit' : 'hidden'},
                size=5,
                label="Dežurni tehnik",
                
            ),
    ),

    atapi.LinesField(
    'izobrazevanje',        
    searchable = True,
    storage=atapi.AnnotationStorage(),
    vocabulary="getSampleVocabulary40",        
    widget=atapi.InAndOutWidget(
                visible = {'view' : 'invisible', 
               'edit' : 'hidden'},
                size=5,
                label="Izobraževanje",
                
            ),
    ),


    atapi.LinesField(
        'bakterioloski_tehnik',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="Urgentni laboratorij",
                    
                ),
    ),


    atapi.LinesField(
        'inoqula_tehnik',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="BMK laboratorij",
                    
                ),
    ),

    atapi.LinesField(
    'sprejem_predpriprava_tehnik',        
    searchable = True,
    storage=atapi.AnnotationStorage(),
    vocabulary="getSampleVocabulary40",        
    widget=atapi.InAndOutWidget(
                size=5,
                label="Sprejem/predpriprava",
                
            ),
    ),

    atapi.LinesField(
        'vpis',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="Vpis",
                    
                ),
    ),



    atapi.LinesField(
        'intervencijska_skupina',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="Intervencijska skupina",
                    
                ),
    ),

    atapi.StringField(
        'intervencijska_skupina_telefon',        
        searchable = True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label="Intervencijska skupina telefon",                    
                ),
    ),





    atapi.LinesField(
        'BOR',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="BOR",
                    
                ),
    ),

    atapi.LinesField(
        'HIV',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="HIV",
                    
                ),
    ),

    atapi.LinesField(
        'HUM',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="HUM",
                    
                ),
    ),

    atapi.LinesField(
        'IT',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="IT",
                    
                ),
    ),

    atapi.LinesField(
        'PRZ',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="PRZ",
                    
                ),
    ),

    atapi.LinesField(
        'KLM',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="KLM",
                    
                ),
    ),

    atapi.LinesField(
        'KOV',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="VZ",
                    
                ),
    ),

    atapi.LinesField(
        'VINVZV',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    visible = {'view' : 'invisible', 
                    'edit' : 'hidden'},
                    size=5,
                    label="VIN (VZV, EBV)",
                    
                ),
    ),

    atapi.LinesField(
        'VINDIF',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    visible = {'view' : 'invisible', 
                    'edit' : 'hidden'},
                    size=5,
                    label="VIN (DIF ali PCR)",
                    
                ),
    ),

    atapi.LinesField(
        'WHO',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="WHO",
                    
                ),
    ),


    atapi.LinesField(
        'kiestra',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=5,
                    label="Kiestra",
                    
                ),
    ),





    atapi.BooleanField(
        'klukca',
	storage=atapi.AnnotationStorage(),               
        widget=atapi.BooleanWidget(
                    label="Kopiraj to stanje pripravljenosti na cel tekoči teden",
                    
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
    """Description of the Example Type"""
    implements(Idezurstvo)

    meta_type = "dezurstvo"
    schema = dezurstvoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    dezurni_zdravnik = atapi.ATFieldProperty('dezurni_zdravnik')
    nadzorni_zdravnik = atapi.ATFieldProperty('nadzorni_zdravnik')
    sarsifon = atapi.ATFieldProperty('sarsifon')
    specializant = atapi.ATFieldProperty('specializant')
    dezurni_tehnik = atapi.ATFieldProperty('dezurni_tehnik')
    izobrazevanje = atapi.ATFieldProperty('izobrazevanje')
    bakterioloski_tehnik = atapi.ATFieldProperty('bakterioloski_tehnik')
    inoqula_tehnik = atapi.ATFieldProperty('inoqula_tehnik')
    sprejem_predpriprava_tehnik = atapi.ATFieldProperty('sprejem_predpriprava_tehnik')
    vpis = atapi.ATFieldProperty('vpis')
    intervencijska_skupina = atapi.ATFieldProperty('intervencijska_skupina')
    intervencijska_skupina_telefon = atapi.ATFieldProperty('intervencijska_skupina_telefon')

    BOR = atapi.ATFieldProperty('BOR')
    HIV = atapi.ATFieldProperty('HIV')
    HUM = atapi.ATFieldProperty('HUM')
    PRZ = atapi.ATFieldProperty('PRZ')
    IT = atapi.ATFieldProperty('IT')
    KLM = atapi.ATFieldProperty('KLM')
    KOV = atapi.ATFieldProperty('KOV')
    VINVZV = atapi.ATFieldProperty('VINVZV')
    VINDIF = atapi.ATFieldProperty('VINDIF')
    WHO = atapi.ATFieldProperty('WHO')
    kiestra = atapi.ATFieldProperty('kiestra')
    
    klukca = atapi.ATFieldProperty('klukca')


    def getSampleVocabulary40(self):
        obj = self.portal.restrictedTraverse('dezurstva/seznam_zaposlenih')
        obj = obj.getFolderContents(contentFilter={'sort_on':'getObjPositionInParent'})             
                                 
        xx = []
        for rows in obj:
                if rows.id != "" and not rows.getObject().getExcludeFromNav():
                        xx.append((rows.id, rows.getObject().Title()))
        
        return DisplayList(xx)

    security = ClassSecurityInfo()

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

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    def excel_export(self, first_day, last_day, oseba):
    
        dezurstva = self.portal_catalog(portal_type = "dezurstvo")
        #print dezurstva, first_day, last_day
        #for x in dezurstva:
        #    print x.id
        dezurstva = [x for x in dezurstva if 'undefined' not in x.id and x.id != 'objekt-za-seznam-zaposlenih-v-formi-spremeni-dezurstvo-ne-brisi' and DateTime.DateTime(x.id) >= first_day and DateTime.DateTime(x.id) <= last_day]

        if oseba:
            dezurstva = [self.portal_catalog(dezurni_zdravnik = oseba, id = x.id)[0] for x in dezurstva if len(self.portal_catalog(dezurni_zdravnik = oseba, id = x.id)) > 0]
        
        
        # create zip file
        #zipdat = StringIO()
        #zf = ZipFile(zipdat, mode='w')

        # create excel
        workBookDocument = xlwt.Workbook()
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

        count = 3
        for j, i in enumerate(dezurstva):
            datum = '.'.join([i.id.split('-')[2], i.id.split('-')[1], i.id.split('-')[0]])
            i = i.getObject()
            #print(i.id)      
            lista = i.dezurni_zdravnik
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"dežurni zdravnik")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.nadzorni_zdravnik
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"nadzorni zdravnik")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.specializant
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"specializant na usposabljanju")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))
            '''
            lista = i.dezurni_tehnik
            print lista
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"dežurni tehnik")
                    person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                    docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    
            lista = i.izobrazevanje
            
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"izobraževanje")
                    person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                    docSheet1.write(count, 2, person.Title().decode('utf-8'))
            '''
            lista = i.bakterioloski_tehnik
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"bakteriološki tehnik")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.inoqula_tehnik
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"inoqula tehnik")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))


            lista = i.sprejem_predpriprava_tehnik
            # To tukaj na silo dodajam ker sem preko plone admina odstranil, ampak naj se ve da so to šifro odpustil...
            if i.id == '2019-06-13':
                lista = ('418206', lista[0])
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"sprejem/predpriprava tehnik")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.vpis
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"vpis")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))


            lista = i.intervencijska_skupina
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"intervencijska_skupina")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))


            lista = i.BOR
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"BOR")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.HIV
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"HIV")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.HUM
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"HUM")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.PRZ
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"PRZ")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.IT
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"IT")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.KLM
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"KLM")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.KOV
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"KOV")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.VINVZV
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"VIN (VZV, EBV)")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.VINDIF
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"VIN (DIF ali PCR)")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.WHO
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"WHO")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))

            lista = i.kiestra
            #print("HEJ: ", lista)
            for h in lista:
                if not oseba or (oseba and oseba == h): 
                    count += 1
                    docSheet1.write(count, 0, datum)
                    docSheet1.write(count, 1, u"Kiestra")
                    try:
                        person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/' + h)
                        docSheet1.write(count, 2, person.Title().decode('utf-8'))
                    except:
                        docSheet1.write(count, 2, ('sodelavec s šifro '+h+' ne obstaja več').decode('utf-8'))


	    #count += 1
            #docSheet1.write(count, 0, '')


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



    def ustvari_cel_teden(self):
	if self.klukca == 1:	
	    parent = self.aq_parent
	    datum = self.title
	    dezurstva = self.portal_catalog(portal_type = "dezurstvo")
	    dezurstva = [x for x in dezurstva if x.id != 'dezurstva/objekt-za-seznam-zaposlenih-v-formi-spremeni-dezurstvo-ne-brisi']
	    dt = datetime.strptime(datum, '%Y-%m-%d')
	    start = dt - timedelta(days=dt.weekday())
	    end = start + timedelta(days=6)
	    for i in range (0,7):
		try:	        
			dezurstvo = parent.invokeFactory(                                                                    
			    type_name='dezurstvo',
			    id=start.strftime("%Y-%m-%d"),
			    title=start.strftime("%Y-%m-%d"),
			    BOR=self.BOR,
			    HIV=self.HIV,
			    HUM=self.HUM,
			    PRZ=self.PRZ,
			    IT=self.IT,
			    KLM=self.KLM,
			    KOV=self.KOV,
			    VINVZV=self.VINVZV,
			    VINDIF=self.VINDIF,
			    WHO=self.WHO,
			    kiestra=self.kiestra,
			)
			#dezurstvo = parent.portal_catalog(portal_type = "dezurstvo", id = start.strftime("%Y-%m-%d"))[0].getObject()  	
			#dezurstvo.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")
		except BadRequest: # to se zgodi, ce npr. ze obstaja objekt za ponedeljek, ki ni imel klukce, potem pa uporabnik naredi nov objekt v torek, kjer je klukca == 1. Takrat je treba tudi ponedeljku spremeniti stanje pripravljenosti
		    for x in dezurstva: #tukaj gremo cez cel seznam dezurstev. To verjetno ni najbolj optimalno.
			dez = x.getObject()
			if dez.id == start.strftime("%Y-%m-%d"):
			    	dez.BOR=self.BOR
				dez.HIV=self.HIV
				dez.HUM=self.HUM
				dez.PRZ=self.PRZ
				dez.IT=self.IT
				dez.KLM=self.KLM
				dez.KOV=self.KOV
				dez.VINVZV=self.VINVZV
				dez.VINDIF=self.VINDIF			    
				dez.WHO = self.WHO	
				dez.kiestra=self.kiestra
		try:		
		    dezurstvo = self.portal_catalog(portal_type = "dezurstvo", id = start.strftime("%Y-%m-%d"))[0].getObject()
		    dezurstvo.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")		
		except WorkflowException:		
		    print("Already published")			
		#workflowTool = getToolByName(self, "portal_workflow")		
		#workflowTool.doActionFor(dezurstvo, "publish")		
		#dezurstvo.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")
				
				
		start = start + timedelta(days=1)
		self.klukca = 0
	
    security.declareProtected(ModifyPortalContent, 'at_post_edit_script')
    def at_post_edit_script(self):	
	self.ustvari_cel_teden()
	#self.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")	

    
    security.declareProtected(ModifyPortalContent, 'at_post_create_script')
    def at_post_create_script(self):
	self.ustvari_cel_teden()	
	#self.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")


atapi.registerType(dezurstvo, PROJECTNAME)
