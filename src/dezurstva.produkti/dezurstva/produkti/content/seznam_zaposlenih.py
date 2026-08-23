"""Definition of the seznam_zaposlenih content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from dezurstva.produkti.interfaces import Iseznam_zaposlenih
from dezurstva.produkti.config import PROJECTNAME

from Products.CMFCore.exceptions import BadRequest
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import *

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

import os
from zipfile import ZipFile
import mimetypes
from StringIO import StringIO
from DateTime.DateTime import DateTime

import base64
import cStringIO
import xlrd
import os, re

import csv
import logging
from Products.CMFPlone.utils import safe_unicode

log = logging.getLogger("Plone")

seznam_zaposlenihSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.FileField(
        'datoteka1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=(u"Datoteka z zaposlenimi"),
            description=(u""),
        ),
        validators=('isNonEmptyFile'),
        
    ),

    atapi.FileField(
        'datoteka2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=(u"Dodaj telefonske"),
            description=(u""),
        ),
        validators=('isNonEmptyFile'),
        
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

seznam_zaposlenihSchema['title'].storage = atapi.AnnotationStorage()
seznam_zaposlenihSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    seznam_zaposlenihSchema,
    folderish=True,
    moveDiscussion=False
)


class seznam_zaposlenih(folder.ATFolder):
    """Description of the Example Type"""
    implements(Iseznam_zaposlenih)

    meta_type = "seznam_zaposlenih"
    schema = seznam_zaposlenihSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    datoteka1 = atapi.ATFieldProperty('datoteka1')
    datoteka2 = atapi.ATFieldProperty('datoteka2')

    security = ClassSecurityInfo()        
    
    
    security.declarePrivate('unpackArchive')
    def unpackArchive(self):
                
        
        field1 = self.getField('datoteka1')
        filetype1 = field1.getContentType(self)
        file1 = field1.getRaw(self)

        field2 = self.getField('datoteka2')
        filetype2 = field2.getContentType(self)
        file2 = field2.getRaw(self)

        msg = self.plone_utils.addPortalMessage
        
        
        if file1.data:       
            

            import datetime
            import re
            filename1 = field1.getFilename(self)
            
            # get the full binary from file
            try:
                chunk1 = file1.data
                filedata1 = ''
                while chunk1 is not None:
                    filedata1 += chunk1.data
                    chunk1 = chunk1.next               
            except AttributeError:
                filedata1 = file1.data

            wb = xlrd.open_workbook(file_contents = filedata1)
            sh = wb.sheet_by_index(0)

                       
            
            
            
            for i in range(sh.nrows):
                row = sh.row_values(i)
                
                try: 
                    sifra = row[0].decode("utf-8")
                except:
                    sifra = ""
                try: 
                    delavec = row[1].encode("utf-8")
                except:
                    delavec = ""
                try: 
                    kontakt = row[2].decode("utf-8")
                except:
                    kontakt = ""
                
                preiskava = self.invokeFactory(
                                                                    
                                        type_name='Folder',
                                        id=sifra,
                                        title=delavec,
                                        description=kontakt                             
                                    )
                
        field1.set(self, 'DELETE_FILE')

        if file2.data: 

            import datetime
            import re
            filename2 = field2.getFilename(self)
            
            # get the full binary from file
            try:
                chunk2 = file2.data
                filedata2 = ''
                while chunk2 is not None:
                    filedata2 += chunk2.data
                    chunk2 = chunk2.next               
            except AttributeError:
                filedata2 = file2.data

            wb = xlrd.open_workbook(file_contents = filedata2)
            sh = wb.sheet_by_index(0)
            

            
            for i in range(sh.nrows):
                row = sh.row_values(i) 

                try: 
                    sifra = row[0].decode("utf-8")
                except:
                    sifra = ""
                try: 
                    delavec = row[1].encode("utf-8")
                except:
                    delavec = ""
                try: 
                    kontakt = row[2].decode("utf-8")
                except:
                    kontakt = ""
                try: 
                    email = row[3].decode("utf-8")
                except:
                    email = ""

                zadetek = self.portal_catalog(id=sifra)

                if zadetek:
                    zadetek = zadetek[0].getObject()
                    if email == '': email = '-'
                    zadetek.setDescription(kontakt + '|' + email)
                    print zadetek.Description()
                else:
                    if sifra != '':
                        print sifra + ' ustvarjen'
                        if email == '': email = '-'
                        preiskava = self.invokeFactory(
                                                                        
                                            type_name='Folder',
                                            id=sifra,
                                            title=delavec,
                                            description=(kontakt + '|' + email)                        
                                        )
                    


        field2.set(self, 'DELETE_FILE')  

    security.declareProtected(ModifyPortalContent, 'at_post_create_script')
    def at_post_create_script(self):
        self.unpackArchive()

    security.declareProtected(ModifyPortalContent, 'at_post_edit_script')
    def at_post_edit_script(self):
        self.unpackArchive()

atapi.registerType(seznam_zaposlenih, PROJECTNAME)
