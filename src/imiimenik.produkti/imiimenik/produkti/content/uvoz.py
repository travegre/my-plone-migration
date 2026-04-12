# -*- encoding: utf-8 -*-

"""Definition of the uvoz content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from imiimenik.produkti.interfaces import Iuvoz
from imiimenik.produkti.config import PROJECTNAME

from imiimenik.produkti import produktiMessageFactory as _

from Products.CMFCore.exceptions import BadRequest
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import *

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

import os
from zipfile import ZipFile
import mimetypes
from StringIO import StringIO

import csv

uvozSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    
    atapi.FileField(
        'datoteka',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Datoteka"),
            description=_(u""),
        ),
        validators=('isNonEmptyFile'),
        
    ),

    atapi.FileField(
        'datoteka2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Datoteka s strukturo podrocij"),
            description=_(u""),
        ),
        validators=('isNonEmptyFile'),
        
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

uvozSchema['title'].storage = atapi.AnnotationStorage()
uvozSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    uvozSchema,
    folderish=True,
    moveDiscussion=False
)


class uvoz(folder.ATFolder):
    """Description of the Example Type"""
    implements(Iuvoz)

    meta_type = "uvoz"
    schema = uvozSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    datoteka = atapi.ATFieldProperty('datoteka')
    datoteka2 = atapi.ATFieldProperty('datoteka2')
    
    security = ClassSecurityInfo()
    
    
    security.declarePrivate('unpackArchive')
    def unpackArchive(self):
                      
        field = self.getField('datoteka')
        filetype = field.getContentType(self)
        file = field.getRaw(self)

        field2 = self.getField('datoteka2')
        filetype2 = field2.getContentType(self)
        file2 = field2.getRaw(self)
                
        if file2.data:

            try:
                chunk = file2.data
                filedata2 = ''
                while chunk is not None:
                    filedata2 += chunk.data
                    chunk = chunk.next
            except AttributeError:
                filedata2 = file2.data
         
                       
            import datetime
            import re
            

            
            m1 = re.finditer('\n(("[^"]*";)|([^("|;)]*;)){2}(("[^"]*")|([^("|;|\n)]*)){1}', filedata2)
            podatki = []
            
            
            
            for h in m1:                        
                podatki.append(h.group(0))

            oddelki = {}
    

            ignoreLine = 0
            for row in podatki: 
                if ignoreLine < 1:
                    ignoreLine = ignoreLine + 1 
                    continue
                else:
                    m = re.finditer('"([^"]+?)";?|([^;]+);?|;|(;;)"', row)                
                    row = []                    
                    for h in m:
                        row.append(h.group(0)[:-1])
                    

                    oddelki[row[0].strip().replace('"', "")] = [''.join(j for j in row[2].strip().replace('"', "").replace(' ', '-') if (ord(j)<123 and ord(j)>96) or (ord(j) == 45) or (ord(j)<91 and ord(j)>64) or (ord(j)<58 and ord(j)>47)), row[2].strip().replace('"', "")]
                    ignoreLine = ignoreLine + 1 
                    continue

            

            for i in oddelki.values():
                nadoddelek = i[0]
                #nadoddelek = ''.join(j for j in nadoddelek if (ord(j)<123 and ord(j)>96) or (ord(j) == 45) or (ord(j)<91 and ord(j)>64) or (ord(j)<58 and ord(j)>47));
                try:
                    mapa = self.portal.restrictedTraverse("portal/data2").invokeFactory(                            
                                type_name='Folder',
                                id=nadoddelek,
                                title=i[1]                                                    
                    )
                except:
                    pass

        if file.data:
            
            self.plone_utils.addPortalMessage('UVOZ PODATKOV:') 
            stevec1 = 0
            stevec2 = 0
            stevec3 = 0
            
            
            filename = field.getFilename(self)

            # get the full binary from file
            try:
                chunk = file.data
                filedata = ''
                while chunk is not None:
                    filedata += chunk.data
                    chunk = chunk.next
            except AttributeError:
                filedata = file.data
         
                       
            import datetime
            import re
            
            
            m1 = re.finditer('\n(("[^"]*";)|([^("|;)]*;)){21}(("[^"]*")|([^("|;|\n)]*)){1}', filedata)
            podatki = []
            
            for h in m1:  
                #self.plone_utils.addPortalMessage(h.group(0)[:-1].decode('utf-8'))               
                podatki.append(h.group(0)[:-1])

            
            #self.plone_utils.addPortalMessage(podatki[-1].decode('utf-8')) 

            
            self.plone_utils.addPortalMessage('Stevilo vseh zaznanih vrstic v datoteki ' + filename + ': ' + str(len(podatki)))                 
            
            
            ignoreLine = 0
            for count, row in enumerate(podatki):
                
                m = re.finditer('"([^"]+?)";?|([^;]+);?|;|(;;)"', row)                
                row = []                    
                
                for h in m:
                    row.append(h.group(0)[:-1])
                
                if row[0].strip().replace('"', "") == "#ODDELEK":
                    oddelek = row[1].strip().replace('"', "")
                    if not podatki[count+3].strip().startswith('"#'):
                        
                        m = re.finditer('"([^"]+?)";?|([^;]+);?|;|(;;)"', podatki[count+3])                
                        row2 = []                   
                
                        for h in m:
                            row2.append(h.group(0)[:-1])                        

                        sifra = row2[0].strip().replace('"', "")

                        oddelek2 = ''.join(i for i in oddelek.replace(' ', '-') if (ord(i)<123 and ord(i)>96) or (ord(i) == 45) or (ord(i)<91 and ord(i)>64) or (ord(i)<58 and ord(i)>47));

                        if sifra in oddelki.keys():
                            podrejeno = True                           
                            try:
                                mapa = self.portal.restrictedTraverse("portal/data2/" + oddelki[sifra][0]).invokeFactory(                            
                                                type_name='Folder',
                                                id=oddelek2,
                                                title=oddelek                                                     
                                )
                            except:
                                pass
                            mapa = self.portal.restrictedTraverse("portal/data2/" + oddelki[sifra][0] + '/' + oddelek2)
                            self.plone_utils.addPortalMessage('ustvarjena mapa: ' + oddelki[sifra][0] + '/' + oddelek2)
                        else:
                            podrejeno = False

                            try:
                                mapa = self.portal.restrictedTraverse("portal/data2").invokeFactory(                            
                                                type_name='Folder',
                                                id=oddelek2,
                                                title=oddelek                                                     
                                )
                            except:
                                pass
                            mapa = self.portal.restrictedTraverse("portal/data2/" + oddelek2)
                            self.plone_utils.addPortalMessage('ustvarjena mapa: ' + oddelek2)
                                

                if not row[0].strip().replace('"', "").startswith('#'):
                                                    
                    
                    try: 
                      predime = row[5].strip().replace('"', "")
                    except:
                      predime = ""
                    try: 
                      ime = row[6].strip().replace('"', "")
                    except:
                      ime = ""
                    try: 
                      priimek = row[7].strip().replace('"', "")
                    except:
                      priimek = ""
                    try: 
                      zaime = row[8].strip().replace('"', "")
                    except:
                      zaime = ""
                    try:
                      telefon = row[12].strip().replace('"', "")
                    except:
                      telefon = ""
                    try: 
                      vuporabi = row[3].strip().replace('"', "")
                    except:
                      vuporabi = ""
                    try: 
                      maticna = row[4].strip().replace('"', "")
                    except:
                      maticna = ""
                    try: 
                      opis = row[9].strip().replace('"', "")
                    except:
                      opis = ""
                    try: 
                      enota = row[10].strip().replace('"', "")
                    except:
                      enota = ""
                    try: 
                      lokacija = row[11].strip().replace('"', "")
                    except:
                      lokacija = ""
                    try: 
                      dodatna = row[13].strip().replace('"', "")
                    except:
                      dodatna = ""
                    try: 
                      dect = row[14].strip().replace('"', "")
                    except:
                      dect = ""
                    try: 
                      fax = row[15].strip().replace('"', "")
                    except:
                      fax = ""  
                    try: 
                      mobilna = row[17].strip().replace('"', "")
                    except:
                      mobilna = ""           
                    try: 
                      multitone = row[16].strip().replace('"', "")
                    except:
                      multitone = ""
                    try: 
                      zunanja = row[18].strip().replace('"', "")
                    except:
                      zunanja = ""
                    try: 
                      enaslov = row[19].strip().replace('"', "")
                    except:
                      enaslov = ""
                    try: 
                      zenaslov = row[20].strip().replace('"', "")
                    except:
                      zenaslov = ""
                    try: 
                      star = row[21].strip().replace('"', "")
                    except:
                      star = ""
                    try: 
                      ID = row[1].strip().replace('"', "")
                    except:
                      ID = ""
                    
                    
                        
                    #now = datetime.datetime.now()
                    novid = ime + '_' + priimek + '_' + ID
                    novid = ''.join(i for i in novid if (ord(i)<123 and ord(i)>96) or (ord(i)<91 and ord(i)>64) or (ord(i)<58 and ord(i)>47));
                    
                   
                    zadetek = self.portal.portal_catalog(portal_type="produkti", review_state='published', id=novid)
                    if zadetek:
                          continue
                          zadetek = zadetek[0].getObject()                      
                                                  
                          zadetek.predime=predime
                          zadetek.ime=ime
                          zadetek.priimek=priimek                          
                          zadetek.zaime=zaime
                          zadetek.telefon=telefon
                          zadetek.oddelek=oddelek
                          zadetek.vuporabi=vuporabi
                          zadetek.maticna=maticna
                          zadetek.opis=opis
                          zadetek.enota=enota
                          zadetek.lokacija=lokacija
                          zadetek.dodatna=dodatna
                          zadetek.dect=dect
                          zadetek.fax=fax
                          zadetek.mobilna=mobilna
                          zadetek.multitone=multitone
                          zadetek.zunanja=zunanja
                          zadetek.enaslov=enaslov
                          zadetek.zenaslov=zenaslov
                          zadetek.star=star                   
                          
                        
                          #self.plone_utils.addPortalMessage('Upravicenec ' + novid[:15] + '... je bil posodobljen') 
                          stevec1 = stevec1 + 1
                    else:                  
                        try:                       
                            self.plone_utils.addPortalMessage(row) 
                            produkt = mapa.invokeFactory(                            
                                type_name='produkti',
                                id=novid,
                                title=ime + ' ' + priimek + ' ' + ID,
                                predime=predime,
                                ime=ime,
                                priimek=priimek,                        
                                zaime=zaime,
                                telefon=telefon,
                                oddelek=oddelek,
                                vuporabi=vuporabi,
                                maticna=maticna,
                                opis=opis,
                                enota=enota,
                                lokacija=lokacija,
                                dodatna=dodatna,
                                dect=dect,
                                fax=fax,
                                mobilna=mobilna,
                                multitone=multitone,
                                zunanja=zunanja,
                                enaslov=enaslov,
                                zenaslov=zenaslov,
                                star=star                            
                            )
                            stevec2 = stevec2 + 1
                        except BadRequest:
                            self.plone_utils.addPortalMessage('Neuspesen vnos: ' + novid) 
                            stevec3 = stevec3 + 1
                                
          
            self.plone_utils.addPortalMessage('Posodobljenih vnosov: ' + str(stevec1))
            self.plone_utils.addPortalMessage('Ustvarjenih vnosov: ' + str(stevec2))  
            self.plone_utils.addPortalMessage('Neuspesno obdelanih vrstic: ' + str(stevec3))  
                                      
            field.set(self, 'DELETE_FILE')
            
            
    security.declareProtected(ModifyPortalContent, 'at_post_create_script')
    def at_post_create_script(self):
        self.unpackArchive()

    security.declareProtected(ModifyPortalContent, 'at_post_edit_script')
    def at_post_edit_script(self):
        self.unpackArchive()
        self.status = _('No changes')
    
    
    

atapi.registerType(uvoz, PROJECTNAME)
