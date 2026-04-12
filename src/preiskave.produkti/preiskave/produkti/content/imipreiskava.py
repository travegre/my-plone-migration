# -*- coding: utf-8 -*-
"""Definition of the imipreiskava content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from preiskave.produkti.interfaces import Iimipreiskava
from preiskave.produkti.config import PROJECTNAME

from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import *

from Products.CMFCore.exceptions import BadRequest
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import *

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


imipreiskavaSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        'sifra',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=("Šifra preiskave"),
            description=(u""),
        ),
    ),

    atapi.LinesField(
        'podrocje',
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=("Področje preiskave"),
            description=(u""),
        ),
    ),

    atapi.TextField(
        'sklop',
        searchable = True,
        storage=atapi.AnnotationStorage(),       
        widget=atapi.RichWidget
        (label='Sklop',
        description=(u""),
	        allow_buttons=(            
	        'link',
	        ),
            
        ),
    ),

    atapi.TextField(
        'sinonim',
        searchable = True,
        storage=atapi.AnnotationStorage(),       
        widget=atapi.RichWidget
        (label='Sinonim preiskave',
        description=(u""),
	        allow_buttons=(            
	        'link',
	        ),
            
        ),
    ),

    atapi.StringField(
        'laboratoriji',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=("Laboratoriji"),
            description=(u""),
        ),
    ),

    atapi.TextField(
        'metode',
        storage=atapi.AnnotationStorage(),       
        widget=atapi.RichWidget
        (label='Metode preiskave',
        description=(u""),
            allow_buttons=(            
            'link',
            ),
            
        ),
    ),

    atapi.TextField(
        'opis',
        storage=atapi.AnnotationStorage(),       
        widget=atapi.RichWidget
        (label='Kratek opis preiskave',
        description=(u""),
	        allow_buttons=(            
	        'link',
	        ),
            
        ),
    ),

    atapi.TextField(
        'opombe',
        storage=atapi.AnnotationStorage(),       
        widget=atapi.RichWidget
        (label='Opombe',
        description=(u""),
            allow_buttons=(            
            'link',
            ),
            
        ),
    ),

    atapi.TextField(
        'trajanje',
        storage=atapi.AnnotationStorage(),       
        widget=atapi.RichWidget
        (label='Trajanje preiskave',
        description=(u""),
            allow_buttons=(            
            'link',
            ),
            
        ),
    ),

    atapi.TextField(
        'urnik',
        storage=atapi.AnnotationStorage(),       
        widget=atapi.RichWidget
        (label='Urnik izvajanja preiskave',
        description=(u""),
            allow_buttons=(            
            'link',
            'bold'
            ),
            
        ),
    ),

    atapi.StringField(
        'link_sop',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=("Link SOP"),
            description=(u""),
        ),
    ),

    atapi.StringField(
        'nova_pre',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=("Nova preiskava"),
            description=(u""),
        ),
    ),

    atapi.StringField(
        'nujna_pre',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=("Nujna preiskava"),
            description=(u""),
        ),
    ),

    atapi.StringField(
        'vzorci',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),              
        widget=atapi.LinesWidget(        			
		label="Vzorci",                    
	),
    ),
    atapi.LinesField(
        'preiskava_vzorec_nujno',
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=("Preiskava Vzorec Nujno"),
            description=(u""),
        ),
    ),
    
    atapi.StringField(
        'vzorci_lab_kratica',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=("Kratica laboratorija"),
            description=(u""),
        ),
    ),
    
    atapi.StringField(
        'vzorci_lab',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),              
        widget=atapi.LinesWidget(        			
	    label="Laboratoriji",                    
	),
    ),
    
    atapi.StringField(
        'vzorci_lab_tel',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),                
        widget=atapi.LinesWidget(        			
	    label="Telefoni",                    
	),
    ),

    atapi.StringField(
        'vzorci_odvzem',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),                
        widget=atapi.LinesWidget(        			
            label="Odvzemi",                    
        ),
    ),

    atapi.StringField(
        'vzorci_odvzem_video_sifra',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),                
        widget=atapi.LinesWidget(        			
            label="Navodilo za odvzem - video sifra",                    
        ),
    ),

    atapi.StringField(
        'vzorci_kolicina',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),                
        widget=atapi.LinesWidget(        			
            label="Količine",                    
        ),
    ),

    atapi.StringField(
        'embalaza_slika_sifra',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),                
        widget=atapi.LinesWidget(        			
            label="EmbalazaSlikaSifra",                    
        ),
    ),


    atapi.StringField(
        'vzorci_transport',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),                
        widget=atapi.LinesWidget(        			
            label="Transporti",                    
        ),
    ),

    atapi.StringField(
        'vzorci_opomba',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),                
        widget=atapi.LinesWidget(        			
            label="Opomba za klinika",                    
        ),
    ),


    atapi.StringField(
        'vzorci_nivo1',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),              
        widget=atapi.LinesWidget(        			
            label="Vzorci nivo1",                    
        ),
    ),
    
    atapi.StringField(
        'vzorci_nivo2',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),              
        widget=atapi.LinesWidget(        			
            label="Vzorci nivo2",                    
        ),
    ),
    
    atapi.StringField(
        'vzorci_nivo3',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),              
        widget=atapi.LinesWidget(        			
            label="Vzorci nivo3",                    
        ),
    ),

    atapi.StringField(
        'vzorci_nivo4',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),              
        widget=atapi.LinesWidget(                   
            label="Vzorci nivo4",                    
        ),
    ),

    atapi.StringField(
        'vzorci_nivo5',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),              
        widget=atapi.LinesWidget(                   
            label="Vzorci nivo5",                    
        ),
    ),

    atapi.StringField(
        'vzorci_nivo6',        
        searchable = True,
        
        storage=atapi.AnnotationStorage(),              
        widget=atapi.LinesWidget(                   
            label="Vzorci nivo6",                    
        ),
    ),


    atapi.FileField(
        'datoteka',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=(u"Dodatni opis preiskave"),
            description=(u""),
        ),
        validators=('isNonEmptyFile'),        
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

imipreiskavaSchema['title'].storage = atapi.AnnotationStorage()
imipreiskavaSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(imipreiskavaSchema, folderish=True, moveDiscussion=False)


class imipreiskava(folder.ATFolder):
    """Description of the Example Type"""
    implements(Iimipreiskava)

    meta_type = "imipreiskava"
    schema = imipreiskavaSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    sifra = atapi.ATFieldProperty('sifra')
    podrocje = atapi.ATFieldProperty('podrocje')
    sklop = atapi.ATFieldProperty('sklop')
    sinonim = atapi.ATFieldProperty('sinonim')

    laboratoriji = atapi.ATFieldProperty('laboratoriji')
    metode = atapi.ATFieldProperty('metode')
    opis = atapi.ATFieldProperty('opis')
    opombe = atapi.ATFieldProperty('opombe')
    trajanje = atapi.ATFieldProperty('trajanje')
    urnik = atapi.ATFieldProperty('urnik')
    link_sop = atapi.ATFieldProperty('link_sop')
    nova_pre = atapi.ATFieldProperty('nova_pre')
    nujna_pre = atapi.ATFieldProperty('nujna_pre')

    vzorci = atapi.ATFieldProperty('vzorci') #tukaj noter so spravljeni NAZIVI in NIVOJI
    preiskava_vzorec_nujno = atapi.ATFieldProperty('preiskava_vzorec_nujno')
    vzorci_lab_kratica = atapi.ATFieldProperty('vzorci_lab_kratica')
    vzorci_lab = atapi.ATFieldProperty('vzorci_lab')
    vzorci_lab_tel = atapi.ATFieldProperty('vzorci_lab_tel')

    vzorci_odvzem = atapi.ATFieldProperty('vzorci_odvzem')
    vzorci_odvzem_video_sifra = atapi.ATFieldProperty('vzorci_odvzem_video_sifra')
    vzorci_kolicina = atapi.ATFieldProperty('vzorci_kolicina')
    embalaza_slika_sifra = atapi.ATFieldProperty('embalaza_slika_sifra')
    vzorci_transport = atapi.ATFieldProperty('vzorci_transport')
    vzorci_opomba = atapi.ATFieldProperty('vzorci_opomba')

    vzorci_nivo1 = atapi.ATFieldProperty('vzorci_nivo1')
    vzorci_nivo2 = atapi.ATFieldProperty('vzorci_nivo2')
    vzorci_nivo3 = atapi.ATFieldProperty('vzorci_nivo3')
    vzorci_nivo4 = atapi.ATFieldProperty('vzorci_nivo4')
    vzorci_nivo5 = atapi.ATFieldProperty('vzorci_nivo5')
    vzorci_nivo6 = atapi.ATFieldProperty('vzorci_nivo6')

    datoteka = atapi.ATFieldProperty('datoteka')
    

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
    security = ClassSecurityInfo()
                
    security.declarePrivate('narediMape')
    def narediMape(self):		    
    	    datoteke = self.invokeFactory(				                    
                type_name='Folder_datoteke',
                id='datoteke',
                title='Datoteke'                
                
            )
    	                           
    security.declareProtected(ModifyPortalContent, 'at_post_create_script')
    def at_post_create_script(self):
        if not hasattr(self, "datoteke"):
        	self.narediMape()
        

atapi.registerType(imipreiskava, PROJECTNAME)
