# coding=utf-8
"""Definition of the dezurstvo content type (Dexterity - kiestra)
"""

from zope.interface import implementer
from plone.dexterity.content import Container
from AccessControl import ClassSecurityInfo

from kiestra.produkti.interfaces import Idezurstvo

import openpyxl
from io import BytesIO


@implementer(Idezurstvo)
class dezurstvo(Container):
    """Dexterity-based dezurstvo content type for kiestra."""

    meta_type = "dezurstvo"
    portal_type = "dezurstvo"

    security = ClassSecurityInfo()

    def getSampleVocabulary40(self):
        obj = self.portal.restrictedTraverse('dezurstva/seznam_zaposlenih')
        obj = obj.getFolderContents(contentFilter={'sort_on':'getObjPositionInParent'})
        xx = []
        for rows in obj:
            if rows.id != "" and not rows.getObject().getExcludeFromNav():
                xx.append((rows.id, rows.getObject().Title()))
        return xx
