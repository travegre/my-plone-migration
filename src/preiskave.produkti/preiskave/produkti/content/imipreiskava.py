# -*- coding: utf-8 -*-
"""Definition of the imipreiskava content type (Dexterity)
"""

from zope.interface import implementer
from plone.dexterity.content import Container
from AccessControl import ClassSecurityInfo
from zope.lifecycleevent.interfaces import IObjectCreatedEvent

from preiskave.produkti.interfaces import Iimipreiskava


@implementer(Iimipreiskava)
class imipreiskava(Container):
    """Dexterity-based imipreiskava content type."""

    meta_type = "imipreiskava"
    portal_type = "imipreiskava"

    # Field attributes
    sifra = u""
    podrocje = ()
    sklop = u""
    sinonim = u""
    laboratoriji = u""
    metode = u""
    opis = u""
    opombe = u""
    trajanje = u""
    urnik = u""
    link_sop = u""
    nova_pre = u""
    nujna_pre = u""
    vzorci = ()
    preiskava_vzorec_nujno = ()
    vzorci_lab_kratica = ()
    vzorci_lab = ()
    vzorci_lab_tel = ()
    vzorci_odvzem = ()
    vzorci_odvzem_video_sifra = ()
    vzorci_kolicina = ()
    embalaza_slika_sifra = ()
    vzorci_transport = ()
    vzorci_opomba = ()
    vzorci_nivo1 = ()
    vzorci_nivo2 = ()
    vzorci_nivo3 = ()
    vzorci_nivo4 = ()
    vzorci_nivo5 = ()
    vzorci_nivo6 = ()
    datoteka = None

    security = ClassSecurityInfo()

    security.declarePrivate('narediMape')
    def narediMape(self):
        datoteke = self.invokeFactory(
            type_name='Folder',
            id='datoteke',
            title='Datoteke'
        )


def on_object_created(obj, event):
    if not hasattr(obj, "datoteke"):
        obj.narediMape()
