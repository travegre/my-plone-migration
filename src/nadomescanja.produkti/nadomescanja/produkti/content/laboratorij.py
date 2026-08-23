# coding=utf-8
"""Definition of the laboratorij content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from nadomescanja.produkti.interfaces import Ilaboratorij
from nadomescanja.produkti.config import PROJECTNAME

from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import *

from Products.CMFCore.exceptions import BadRequest
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import *
from Products.CMFCore import permissions as CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.CMFCore.utils import getToolByName
import os
from zipfile import ZipFile
import mimetypes
from StringIO import StringIO
import base64
import cStringIO
import sys
import random
import DateTime

laboratorijSchema = folder.ATFolderSchema.copy() + atapi.Schema((

  
    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        'okrajsava',        
        searchable = True,
        required=True,
        storage=atapi.AnnotationStorage(),        
        widget=atapi.StringWidget(
                    label=u"Okrajšava",                    
                ),
    ),

    atapi.LinesField(
        'privzeti_vodja',        
        searchable = True,
        storage=atapi.AnnotationStorage(),
        vocabulary="getSampleVocabulary40",        
        widget=atapi.InAndOutWidget(
                    size=8,
                    label=u"Privzeti vodja",
                    
                ),
    )
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

laboratorijSchema['title'].storage = atapi.AnnotationStorage()
laboratorijSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    laboratorijSchema,
    folderish=True,
    moveDiscussion=False
)


class laboratorij(folder.ATFolder):
    add_permission = "nadomescanja.produkti: Add laboratorij"

    """Description of the Example Type"""
    implements(Ilaboratorij)

    meta_type = "laboratorij"
    schema = laboratorijSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    okrajsava = atapi.ATFieldProperty('okrajsava')
    privzeti_vodja = atapi.ATFieldProperty('privzeti_vodja')

    def getSampleVocabulary40(self):
        portal = getToolByName(self, 'portal_url').getPortalObject()
        try:
            folder = portal.unrestrictedTraverse('dezurstva/seznam_zaposlenih')
            xx = []
            for obj in folder.objectValues():
                if obj.id != "" and not obj.getExcludeFromNav():
                    xx.append((obj.id, obj.Title()))
            return DisplayList(xx)
        except Exception:
            return DisplayList([])

    security = ClassSecurityInfo()

    def at_post_create_script(self):
        """Called once, right after the object is first created."""
        wf = getToolByName(self, 'portal_workflow')
        try:
            wf.doActionFor(self, 'publish')
        except Exception:
            pass

    def at_post_edit_script(self):
        """Called every time the object is saved/edited."""
        pass  # put anything you want to run on every save here

atapi.registerType(laboratorij, PROJECTNAME)

