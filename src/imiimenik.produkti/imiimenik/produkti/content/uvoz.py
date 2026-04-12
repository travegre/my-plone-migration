# -*- encoding: utf-8 -*-

"""Definition of the uvoz content type (Dexterity)
"""

from zope.interface import implementer
from plone.dexterity.content import Container
from AccessControl import ClassSecurityInfo
from Products.CMFCore.exceptions import BadRequest
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from zope.lifecycleevent.interfaces import IObjectCreatedEvent, IObjectModifiedEvent

import plone.api
from imiimenik.produkti.interfaces import Iuvoz
from imiimenik.produkti import produktiMessageFactory as _

import csv
import re


@implementer(Iuvoz)
class uvoz(Container):
    """Dexterity-based uvoz content type."""

    meta_type = "uvoz"
    portal_type = "uvoz"

    datoteka = None
    datoteka2 = None

    security = ClassSecurityInfo()
    
    
    security.declarePrivate('unpackArchive')
    def unpackArchive(self):
                      
        field_name = 'datoteka'
        
        file = getattr(self, 'datoteka', None)

        field2_name = 'datoteka2'
        
        file2 = getattr(self, 'datoteka2', None)
                
        if file2 and getattr(file2, 'data', None):

            try:
                chunk = file2.data if hasattr(file2, 'next') else None
                filedata2 = b''
                while chunk is not None:
                    filedata2 += chunk.data if isinstance(chunk.data, bytes) else chunk.data.encode('utf-8')
                    chunk = chunk.next
            except AttributeError:
                filedata2 = file2.data if isinstance(file2.data, bytes) else file2.data.encode('utf-8')
         
                       
            import datetime
            import re

            filedata2_str = filedata2.decode('utf-8', errors='replace') if isinstance(filedata2, bytes) else filedata2
            m1 = re.finditer('\n(("[^"]*";)|([^("|;)]*;)){2}(("[^"]*")|([^("|;|\n)]*)){1}', filedata2_str)
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
                    mapa = plone.api.portal.get().restrictedTraverse("portal/data2").invokeFactory(                            
                                type_name='Folder',
                                id=nadoddelek,
                                title=i[1]                                                    
                    )
                except:
                    pass

        if file and getattr(file, 'data', None):
            
            plone.api.portal.show_message(message='UVOZ PODATKOV:', request=self.REQUEST) 
            stevec1 = 0
            stevec2 = 0
            stevec3 = 0
            
            
            filename = getattr(file, 'filename', 'file.csv')

            # get the full binary from file
            try:
                chunk = file.data if hasattr(file, 'next') else None
                filedata = b''
                while chunk is not None:
                    filedata += chunk.data if isinstance(chunk.data, bytes) else chunk.data.encode('utf-8')
                    chunk = chunk.next
            except AttributeError:
                filedata = file.data if isinstance(file.data, bytes) else file.data.encode('utf-8')
         
                       
            import datetime
            import re
            
            
            filedata_str = filedata.decode('utf-8', errors='replace') if isinstance(filedata, bytes) else filedata
            m1 = re.finditer('\n(("[^"]*";)|([^("|;)]*;)){21}(("[^"]*")|([^("|;|\n)]*)){1}', filedata_str)
            podatki = []
            
            for h in m1:  
                #plone.api.portal.show_message(message=h.group(0)[:-1].decode('utf-8'), request=self.REQUEST)               
                podatki.append(h.group(0)[:-1])

            
            #plone.api.portal.show_message(message=podatki[-1].decode('utf-8'), request=self.REQUEST) 

            
            plone.api.portal.show_message(message='Stevilo vseh zaznanih vrstic v datoteki ' + filename + ': ' + str(len(podatki)), request=self.REQUEST)                 
            
            
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
                                mapa = plone.api.portal.get().restrictedTraverse("portal/data2/" + oddelki[sifra][0]).invokeFactory(                            
                                                type_name='Folder',
                                                id=oddelek2,
                                                title=oddelek                                                     
                                )
                            except:
                                pass
                            mapa = plone.api.portal.get().restrictedTraverse("portal/data2/" + oddelki[sifra][0] + '/' + oddelek2)
                            plone.api.portal.show_message(message='ustvarjena mapa: ' + oddelki[sifra][0] + '/' + oddelek2, request=self.REQUEST)
                        else:
                            podrejeno = False

                            try:
                                mapa = plone.api.portal.get().restrictedTraverse("portal/data2").invokeFactory(                            
                                                type_name='Folder',
                                                id=oddelek2,
                                                title=oddelek                                                     
                                )
                            except:
                                pass
                            mapa = plone.api.portal.get().restrictedTraverse("portal/data2/" + oddelek2)
                            plone.api.portal.show_message(message='ustvarjena mapa: ' + oddelek2, request=self.REQUEST)
                                

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
                    
                   
                    catalog = getToolByName(self, 'portal_catalog')
                    zadetek = catalog(portal_type="produkti", review_state='published', id=novid)
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
                          
                        
                          #plone.api.portal.show_message(message='Upravicenec ' + novid[:15] + '... je bil posodobljen', request=self.REQUEST) 
                          stevec1 = stevec1 + 1
                    else:                  
                        try:                       
                            plone.api.portal.show_message(message=row, request=self.REQUEST) 
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
                            plone.api.portal.show_message(message='Neuspesen vnos: ' + novid, request=self.REQUEST) 
                            stevec3 = stevec3 + 1
                                
          
            plone.api.portal.show_message(message='Posodobljenih vnosov: ' + str(stevec1), request=self.REQUEST)
            plone.api.portal.show_message(message='Ustvarjenih vnosov: ' + str(stevec2), request=self.REQUEST)  
            plone.api.portal.show_message(message='Neuspesno obdelanih vrstic: ' + str(stevec3), request=self.REQUEST)  
                                      
            setattr(self, 'datoteka', None)
            
            
def on_object_created(obj, event):
    obj.unpackArchive()


def on_object_modified(obj, event):
    obj.unpackArchive()
        
    
    
    

