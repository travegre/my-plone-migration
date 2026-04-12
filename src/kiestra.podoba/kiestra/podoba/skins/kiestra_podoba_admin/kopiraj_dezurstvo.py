# -*- encoding: utf-8 -*-
## Script (Python) "oddaj_narocilo"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Add multiple items with multiple quantities to cart

from Products.CMFCore.utils import getToolByName





r = container.REQUEST
session = r.SESSION
form = r.form
star = form["star"]
nov = form["nov"]

msg = context.portal.plone_utils.addPortalMessage

obj = context.portal_catalog(portal_type = "dezurstvo", id = star)
obj2 = context.portal_catalog(portal_type = "dezurstvo", id = nov)

if obj2:
  msg(u'Dežurstvo že obstaja.')
  r.RESPONSE.redirect('/kiestra/dezurstva-1/' + nov + '/edit') 
elif obj:
  obj = obj[0].getObject()
  dezurstvo = context['dezurstva-1'].invokeFactory(                                                                    
                type_name='dezurstvo',
                id=nov,
                title=nov,
                priprava_vzorcev=obj.priprava_vzorcev,
                cepljenje_vzorcev=obj.cepljenje_vzorcev,
                odcitavanje=obj.odcitavanje,
                identifikacija=obj.identifikacija,
                antibiogram=obj.antibiogram,
                izolacija=obj.izolacija,
                odpad=obj.odpad,
                ciscenje=obj.ciscenje,
                priprava_vzorcev_text=obj.priprava_vzorcev_text,
                cepljenje_vzorcev_text=obj.cepljenje_vzorcev_text,
                odcitavanje_text=obj.odcitavanje_text,
                identifikacija_text=obj.identifikacija_text,
                antibiogram_text=obj.antibiogram_text,
                izolacija_text=obj.izolacija_text,
                odpad_text=obj.odpad_text,
                ciscenje_text=obj.ciscenje_text,
                stalni_tekst=obj.stalni_tekst
            )

  
  dezurstvo = context.portal_catalog(portal_type = "dezurstvo", id = nov)[0].getObject()
  dezurstvo.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")
  msg(u'Dežurstvo je bilo uspešno kopirano.')
  r.RESPONSE.redirect('/kiestra/dezurstva-1') 
else:
  msg(u'Zaradi napake dežurstvo ni bilo kopirano.')
  r.RESPONSE.redirect('/kiestra/dezurstva-1') 

return printed    
