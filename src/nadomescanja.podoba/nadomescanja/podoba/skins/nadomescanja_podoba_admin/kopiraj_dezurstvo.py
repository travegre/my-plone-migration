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
  msg(u'Nadomeščanje že obstaja.')
  r.RESPONSE.redirect('/nadomescanja/nadomescanja-1/' + nov + '/edit') 
elif obj:
  obj = obj[0].getObject()
  dezurstvo = context['nadomescanja-1'].invokeFactory(                                                                    
                type_name='dezurstvo',
                id=nov,
                title=nov,
                nadomescanja_json=obj.nadomescanja_json
            )

  
  dezurstvo = context.portal_catalog(portal_type = "dezurstvo", id = nov)[0].getObject()
  dezurstvo.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")
  msg(u'Nadomeščanje je bilo uspešno kopirano.')
  r.RESPONSE.redirect('/nadomescanja/nadomescanja-1') 
else:
  msg(u'Zaradi napake nadomeščanje ni bilo kopirano.')
  r.RESPONSE.redirect('/nadomescanja/nadomescanja-1') 

return printed    
