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
datum = form["datum"]

obj = context.portal_catalog(portal_type = "dezurstvo", id = datum)

if obj:
  r.RESPONSE.redirect('/dezurstva/dezurstva-1/'+ datum + '/edit')
else:
  dezurstvo = context['dezurstva-1'].invokeFactory(                                                                    
                type_name='dezurstvo',
                id=datum,
                title=datum                                      
            )
  dezurstvo = context.portal_catalog(portal_type = "dezurstvo", id = datum)[0].getObject()
  
  dezurstvo.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")
  r.RESPONSE.redirect('/dezurstva/dezurstva-1/'+ datum + '/edit')

return printed    
