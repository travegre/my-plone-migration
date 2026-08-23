"""Definition of the produkti content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from imiimenik.produkti.interfaces import Iprodukti
from imiimenik.produkti.config import PROJECTNAME

produktiSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        'predime',
        accessor='Predime',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Predpona"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'ime',
        accessor='Ime',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Ime"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'priimek',
        accessor='Priimek',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Priimek"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'zaime',
        accessor='Zaime',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Zapona"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'oddelek',
        accessor='Oddelek',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Oddelek"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'telefon',
        accessor='Telefon',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Telefon"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'vuporabi',
        accessor='Vuporabi',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"V uporabi"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'maticna',
        accessor='Maticna',
        searchable = False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=("Maticna stevilka"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'opis',
        accessor='Opis',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Opis delovnega mesta"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'enota',
        accessor='Enota',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Enota"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'lokacija',
        accessor='Lokacija',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Lokacija"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'dodatna',
        accessor='Dodatna',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Dodatna"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'dect',
        accessor='Dect',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"DECT"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'fax',
        accessor='Fax',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Fax"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'multitone',
        accessor='Multitone',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Multitone"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'mobilna',
        accessor='Mobilna',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Mobilna"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'zunanja',
        accessor='Zunanja',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Zunanja"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'enaslov',
        accessor='Enaslov',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"E-naslov"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'zenaslov',
        accessor='Zenaslov',
        searchable = True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Zunanji e-naslov"),
            description=(u""),             
        ),        
    ),
    
    atapi.StringField(
        'star',
        accessor='Star',
        searchable = False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=(u"Star zapis"),
            description=(u""),             
        ),        
    ),
    
    

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

produktiSchema['title'].storage = atapi.AnnotationStorage()
produktiSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(produktiSchema, moveDiscussion=False)


class produkti(base.ATCTContent):
    """Description of the Example Type"""
    implements(Iprodukti)

    meta_type = "produkti"
    schema = produktiSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    predime = atapi.ATFieldProperty('predime')
    ime = atapi.ATFieldProperty('ime')
    priimek = atapi.ATFieldProperty('priimek')
    zaime = atapi.ATFieldProperty('zaime')
    oddelek = atapi.ATFieldProperty('oddelek')
    telefon = atapi.ATFieldProperty('telefon')
    vuporabi = atapi.ATFieldProperty('vuporabi')
    maticna = atapi.ATFieldProperty('maticna')
    opis = atapi.ATFieldProperty('opis')
    enota = atapi.ATFieldProperty('enota')
    lokacija = atapi.ATFieldProperty('lokacija')
    dodatna = atapi.ATFieldProperty('dodatna')
    dect = atapi.ATFieldProperty('dect')
    fax = atapi.ATFieldProperty('fax')
    mobilna = atapi.ATFieldProperty('mobilna')
    multitone = atapi.ATFieldProperty('multitone')
    zunanja = atapi.ATFieldProperty('zunanja')
    enaslov = atapi.ATFieldProperty('enaslov')
    zenaslov = atapi.ATFieldProperty('zenaslov')
    star = atapi.ATFieldProperty('star')
    
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(produkti, PROJECTNAME)
