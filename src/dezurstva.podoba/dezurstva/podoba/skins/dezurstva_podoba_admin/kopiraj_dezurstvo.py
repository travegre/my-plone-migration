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
  r.RESPONSE.redirect('/dezurstva/dezurstva-1/' + nov + '/edit') 
elif obj:
  obj = obj[0].getObject()
  dezurstvo = context['dezurstva-1'].invokeFactory(                                                                    
                type_name='dezurstvo',
                id=nov,
                title=nov,
                dezurni_zdravnik=obj.dezurni_zdravnik,
                nadzorni_zdravnik=obj.nadzorni_zdravnik,
                dezurni_tehnik=obj.dezurni_tehnik,
                izobrazevanje=obj.izobrazevanje,
                bakterioloski_tehnik=obj.bakterioloski_tehnik,
                #kiestra_tehnik=obj.kiestra_tehnik,
		inoqula_tehnik=obj.inoqula_tehnik,
		sprejem_predpriprava_tehnik=obj.sprejem_predpriprava_tehnik,
 		#a tukaj manjka se vpis=obj.vpis  ??  - komentar dodal Žiga           
		BOR=obj.BOR,
                HIV=obj.HIV,
                HUM=obj.HUM,
                PRZ=obj.PRZ,
                IT=obj.IT,
                KLM=obj.KLM,
                KOV=obj.KOV,
                VINVZV=obj.VINVZV,
                VINDIF=obj.VINDIF,
                WHO=obj.WHO
            )
  dezurstvo = context.portal_catalog(portal_type = "dezurstvo", id = nov)[0].getObject()
  dezurstvo.portal_workflow.doActionFor(dezurstvo, "publish", comment = "publised programmatically")
  msg(u'Dežurstvo je bilo uspešno kopirano.')
  r.RESPONSE.redirect('/dezurstva/dezurstva-1') 
else:
  msg(u'Zaradi napake dežurstvo ni bilo kopirano.')
  r.RESPONSE.redirect('/dezurstva/dezurstva-1') 

return printed    
