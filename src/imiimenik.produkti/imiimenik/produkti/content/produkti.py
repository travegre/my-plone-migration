"""Definition of the produkti content type (Dexterity)
"""

from zope.interface import implementer
from plone.dexterity.content import Item

from imiimenik.produkti.interfaces import Iprodukti


@implementer(Iprodukti)
class produkti(Item):
    """Dexterity-based produkti content type."""

    meta_type = "produkti"
    portal_type = "produkti"

    # Field attributes are stored as annotations by Dexterity behaviors
    predime = u""
    ime = u""
    priimek = u""
    zaime = u""
    oddelek = u""
    telefon = u""
    vuporabi = u""
    maticna = u""
    opis = u""
    enota = u""
    lokacija = u""
    dodatna = u""
    dect = u""
    fax = u""
    mobilna = u""
    multitone = u""
    zunanja = u""
    enaslov = u""
    zenaslov = u""
    star = u""
