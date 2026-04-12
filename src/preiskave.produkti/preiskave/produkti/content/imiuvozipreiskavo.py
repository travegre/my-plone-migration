# -*- coding: utf-8 -*-
"""Definition of the Imi uvozi preiskavo content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from preiskave.produkti.interfaces import Iimiuvozipreiskavo
from preiskave.produkti.config import PROJECTNAME

from Products.CMFCore.exceptions import BadRequest
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import *

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

import os
from zipfile import ZipFile
import mimetypes
from StringIO import StringIO

import csv
import logging
import xlrd

log = logging.getLogger("Plone")


imiuvozipreiskavoSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.FileField(
        'datoteka1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=(u"Datoteka s preiskavami"),
            description=(u""),
        ),
        validators=('isNonEmptyFile'),
        
    ),
    
    atapi.FileField(
        'datoteka2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=(u"Datoteka z vzorci"),
            description=(u""),
        ),
        validators=('isNonEmptyFile'),
        
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

imiuvozipreiskavoSchema['title'].storage = atapi.AnnotationStorage()
imiuvozipreiskavoSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(imiuvozipreiskavoSchema, moveDiscussion=False)


class imiuvozipreiskavo(base.ATCTContent):
    """Description of the Example Type"""
    implements(Iimiuvozipreiskavo)

    meta_type = "imiuvozipreiskavo"
    schema = imiuvozipreiskavoSchema

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
        
            msg('UVOZ PREISKAV:') 
            stevec1 = 0
            stevec2 = 0
            stevec3 = 0
            
            filename1 = field1.getFilename(self)
            filename2 = field2.getFilename(self)
	
	    #odpremo prvi fajl
	    dat1 = StringIO(file1.data)
	    xl_workbook1 = xlrd.open_workbook(file_contents=dat1.read())
	    xl_sheet1 = xl_workbook1.sheet_by_index(0)
	    
	    #odpremo drugi fajl
	    dat2 = StringIO(file2.data)
	    xl_workbook2 = xlrd.open_workbook(file_contents=dat2.read())
	    xl_sheet2 = xl_workbook2.sheet_by_index(0)

	    msg('Stevilo vseh zaznanih vrstic v datoteki ' + filename1 + ': ' + str(xl_sheet1.nrows))
	    msg('Stevilo vseh zaznanih vrstic v datoteki ' + filename2 + ': ' + str(xl_sheet2.nrows)) 

	    vzorci = {}
            preiskave = {}
            preiskave2 = {}
            povezava = {}
            povezava_sin = {}
            povezava_nivo1 = {}
            povezava_nivo2 = {}
            povezava_nivo3 = {}
            povezava_nivo4 = {}
            povezava_nivo5 = {}
            povezava_lab = {}
            povezava_tel = {}
            povezava_odvzem = {}
            povezava_kolicina = {}
            povezava_transport = {}
            povezava_opomba = {}
	    
	    #SHRANIMO PODATKE OD PREISKAVE
	    for row_idx in range(1, xl_sheet1.nrows):    # Iterate through rows - skip first row, because headers
		row = []
		for col_idx in range(0, xl_sheet1.ncols):  # Iterate through columns
    		    cell_obj = xl_sheet1.cell(row_idx, col_idx)  # Get cell object by row, col
		    row.append(cell_obj.value) #dodamo vrednost iz celice v tabelo

		#print row
		#tle se pol dodelijo stvari
		sifra = str(row[0])
		naziv = row[1]
		podrocje = row[2]
		sklop = row[3]
		sinonim = row[4]

		laboratoriji = row[5] #nov
		metode = row[6]
		opis = row[7]
		opomba = row[8]
		trajanje = row[9]
		urnik = row[10]
		link_sop = row[11] #nov
		nova_pre = str(row[12]) #nov
		nujna_pre = row[13] #nov

		VzorecNaziv = row[14]
		VzorecSifra = str(row[15])
		PreiskavaVzorecNujno = row[16] #nov
		Lab_1 = row[17] #nov
		Lab1 = row[18]
		TelLab1 = str(row[19])
		Lab_2 = row[20] #nov
		Lab2 = row[21]
		TelLab2 = str(row[22])
		Lab_3 = row[23] #nov
		Lab3 = "" #tega ni v novem katalogu for some reason
		TelLab3 = str(row[24])
		NavodiloZaOdvzem = row[25]
		NavodiloZaOdvzemVideoSifra = row[26]
		KolicinaInEmbalaza = row[27]
		EmbalazaSlikaSifra = row[28]
		NavodilaZaTransport = row[29]
		OpombaZaKlinika = row[30]

		try:	                
	            preiskave[sifra][0].append(podrocje)
		    preiskave[sifra][10].append(VzorecSifra)
		    preiskave[sifra][11].append(Lab_1 + '###' + Lab_2 + '###' + Lab_3) #vzorci_lab_kratica
		    preiskave[sifra][12].append(Lab1 + '###' + Lab2 + '###' + Lab3) #vzorci_lab
		    preiskave[sifra][13].append(TelLab1 + '###' + TelLab2 + '###' + TelLab3) #vzorci_lab_tel
              	    preiskave[sifra][14].append(NavodiloZaOdvzem)
              	    preiskave[sifra][15].append(NavodiloZaOdvzemVideoSifra)
		    preiskave[sifra][16].append(KolicinaInEmbalaza)
		    preiskave[sifra][17].append(EmbalazaSlikaSifra)
		    preiskave[sifra][18].append(NavodilaZaTransport)
              	    preiskave[sifra][19].append(OpombaZaKlinika)
		    preiskave[sifra][24].append(PreiskavaVzorecNujno)
	        except:
		    preiskave[sifra] = [[podrocje], sifra, naziv, metode, opis, sinonim, trajanje, urnik, opomba, sklop, [VzorecSifra], [Lab_1 + '###' + Lab_2 + '###' + Lab_3], [Lab1 + '###' + Lab2 + '###' + Lab3], [TelLab1 + '###' + TelLab2 + '###' + TelLab3], [NavodiloZaOdvzem], [NavodiloZaOdvzemVideoSifra], [KolicinaInEmbalaza], [EmbalazaSlikaSifra], [NavodilaZaTransport], [OpombaZaKlinika], laboratoriji, link_sop, nova_pre, nujna_pre, [PreiskavaVzorecNujno]]



		vzorci[VzorecSifra] = VzorecNaziv

		povezava[sifra] = []
		povezava_sin[sifra] = []
		povezava_nivo1[sifra] = []
		povezava_nivo2[sifra] = []
		povezava_nivo3[sifra] = []
		povezava_nivo4[sifra] = []
		povezava_nivo5[sifra] = []
		povezava_lab[sifra] = []
		povezava_tel[sifra] = []
		povezava_odvzem[sifra] = []
		povezava_kolicina[sifra] = []
		povezava_transport[sifra] = []

		povezava_opomba[sifra] = []

	    
	    #SHRANIMO PODATKE OD VZORCEV
	    for row_idx in range(1, xl_sheet2.nrows):    # Iterate through rows - skip first row, because headers
		row = []
		for col_idx in range(0, xl_sheet2.ncols):  # Iterate through columns
    		    cell_obj = xl_sheet2.cell(row_idx, col_idx)  # Get cell object by row, col
		    row.append(cell_obj.value)#dodamo vrednost iz celice v tabelo
		 
	        sifra_vzorca = str(row[0])
		nivo1 = row[1]
		nivo2 = row[2]
	        nivo3 = row[3]
	        nivo4 = row[4]
	        nivo5 = row[5]
	        nivo6 = row[6]
		
	        #naziv in ostali podatki
		vzorci[sifra_vzorca] += '######' + nivo1 + '###' + nivo2 + '###' + nivo3 + '###' + nivo4 + '###' + nivo5 + '###' + nivo6



       	    #ZACNEMO POSODABLJATI/USTVARJATI PREISKAVE
	    preiskave210 = preiskave.keys()

	    for row2 in preiskave210:
		row = preiskave[row2] #lastnosti od ene preiskave
	        novid = "preiskava_" + row2		 
	        zadetek = self.portal_catalog(portal_type="imipreiskava", id=novid)

	        preisk_vzorci = []
		preisk_vzorci_nivo1 = []
		preisk_vzorci_nivo2 = []
		preisk_vzorci_nivo3 = []
		preisk_vzorci_nivo4 = []
		preisk_vzorci_nivo5 = []
		preisk_vzorci_nivo6 = []
		row_vzorci = []
		
		for sifra_vzorca in row[10]:
			row_vzorci.append(vzorci[sifra_vzorca]) #lastnosti od enga vzorca
			nivo = vzorci[sifra_vzorca].split("###")
			print sifra_vzorca
			print nivo
			try:
				preisk_vzorci_nivo1.append(nivo[2])
				preisk_vzorci_nivo2.append(nivo[3])
				preisk_vzorci_nivo3.append(nivo[4])
				preisk_vzorci_nivo4.append(nivo[5])
				preisk_vzorci_nivo5.append(nivo[6])
				preisk_vzorci_nivo6.append(nivo[7])
			except IndexError:
				pass

	        if zadetek:
			print "Posodabljam preiskavo"
			zadetek = zadetek[0].getObject()

			zadetek.podrocje = row[0]
			zadetek.title = row[2]
			zadetek.metode = row[3]								            
			zadetek.opis = row[4]
			zadetek.sinonim = row[5]
			zadetek.trajanje = row[6]
			zadetek.urnik = row[7]
			zadetek.opombe = row[8]
			zadetek.sklop = row[9]

			zadetek.vzorci_lab_kratica = row[11]
			zadetek.vzorci_lab = row[12]
			zadetek.vzorci_lab_tel= row[13]
			zadetek.vzorci_odvzem = row[14]	#NavodiloZaOdvzem
			zadetek.vzorci_odvzem_video_sifra = row[15] #NavodiloZaOdvzemVideoSifra
			zadetek.vzorci_kolicina = row[16] #KolicinaInEmbalaza
			zadetek.embalaza_slika_sifra = row[17] #EmbalazaSlikaSifra
			zadetek.vzorci_transport = row[18] #NavodilaZaTransport
			zadetek.vzorci_opomba = row[19] #OpombaZaKlinika
			zadetek.vzorci = row_vzorci #vsi vzorci za preiskavo
			zadetek.vzorci_nivo1 = preisk_vzorci_nivo1
			zadetek.vzorci_nivo2 = preisk_vzorci_nivo2
			zadetek.vzorci_nivo3 = preisk_vzorci_nivo3
			zadetek.vzorci_nivo4 = preisk_vzorci_nivo4
			zadetek.vzorci_nivo5 = preisk_vzorci_nivo5
			zadetek.vzorci_nivo6 = preisk_vzorci_nivo6

			zadetek.laboratoriji = row[20]
			zadetek.link_sop = row[21]
			zadetek.nova_pre = row[22]
			zadetek.nujna_pre = row[23]
			zadetek.preiskava_vzorec_nujno = row[24]

			#zadetek.reindexObject(idxs=["moj"])
			
			msg('Preiskava ' + novid + ' je bila posodobljena') 
			stevec1 = stevec1 + 1
	        else:
			print "Delam novo preiskavo"
		        try:
		            preiskava = self.portal.restrictedTraverse("portal/preiskave/preiskave-1/katalog-preiskav").invokeFactory(
						type_name='imipreiskava',
						id=novid,
						podrocje = row[0],
						title = row[2],
						metode = row[3],
						opis = row[4],
						sinonim = row[5],
						trajanje = row[6],
						urnik = row[7],
						opombe = row[8],
						sklop = row[9],
						vzorci_lab_kratica = row[11],
						vzorci_lab = row[12],
						vzorci_lab_tel= row[13],
						vzorci_odvzem = row[14],	#NavodiloZaOdvzem
						vzorci_odvzem_video_sifra = row[15], #NavodiloZaOdvzemVideoSifra
						vzorci_kolicina = row[16], #KolicinaInEmbalaza
						embalaza_slika_sifra = row[17], #EmbalazaSlikaSifra
						vzorci_transport = row[18], #NavodilaZaTransport
						vzorci_opomba = row[19], #OpombaZaKlinika
						vzorci = row_vzorci, #vsi vzorci za preiskavo
						vzorci_nivo1 = preisk_vzorci_nivo1,
						vzorci_nivo2 = preisk_vzorci_nivo2,
						vzorci_nivo3 = preisk_vzorci_nivo3,
						vzorci_nivo4 = preisk_vzorci_nivo4,
						vzorci_nivo5 = preisk_vzorci_nivo5,
						vzorci_nivo6 = preisk_vzorci_nivo6,

						laboratoriji = row[20],
						link_sop = row[21],
						nova_pre = row[22],
						nujna_pre = row[23],
						preiskava_vzorec_nujno = row[24]					            
				        )
		            obj = self.portal.restrictedTraverse("portal/preiskave/preiskave-1/katalog-preiskav/" + novid)
		            #obj.content_status_modify(workflow_action='publish')
		            
			    #ce zelimo obdrzati prej nalozene datoteke, tukaj potem ne smemo narediti nove mape Datoteke..mapa Datoteke pa se ze ustvari ob kreiranju nove preiskave
		            #datoteke = obj.invokeFactory(		            
				          #type_name='Folder_datoteke',
				          #id='datoteke',
				          #title='Datoteke'
				      #)
		            #self.portal.restrictedTraverse("www.imi.si/portal/diagnosticna-dejavnost/preiskave/%s/datoteke" % novid).content_status_modify(workflow_action='publish')
		            stevec2 = stevec2 + 1
		            #obj.reindexObject(idxs=["moj"])  
		        except BadRequest:
				        msg('Neuspesen vnos: ' + novid) 
				        stevec3 = stevec3 + 1
           
					            
	                 
        msg('Posodobljenih vnosov: ' + str(stevec1))
        msg('Ustvarjenih vnosov: ' + str(stevec2))  
        msg('Neuspesno obdelanih vrstic: ' + str(stevec3))        		        
                     
        field1.set(self, 'DELETE_FILE')
        field2.set(self, 'DELETE_FILE')
            
            

    security.declareProtected(ModifyPortalContent, 'at_post_create_script')
    def at_post_create_script(self):
        self.unpackArchive()

    security.declareProtected(ModifyPortalContent, 'at_post_edit_script')
    def at_post_edit_script(self):
        self.unpackArchive()
    

atapi.registerType(imiuvozipreiskavo, PROJECTNAME)
