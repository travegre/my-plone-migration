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

obj = context.portal.portal_catalog(portal_type = "dezurstvo", id = datum)

if obj:
  r.RESPONSE.redirect('nastavitve/dezurstva/'+ datum)
else:
  dezurstvo = context['nastavitve']['dezurstva'].invokeFactory(                                                                    
                type_name='dezurstvo',
                id=datum,
                title=datum                                      
            )
  r.RESPONSE.redirect('nastavitve/dezurstva/'+ datum)

return printed    
