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
try:
	izvoz1 = form["izvoz-1-izbira"]
	if izvoz1 == 'oddo':
		od = form["od"]
		do = form["do"]	
		if not (od and do):
			r.RESPONSE.redirect('/nadomescanja') 
except:
	izvoz1 = False
try:
	izvoz2 = form["izvoz-2-oseba"]
	oseba = form["izvoz-2-oseba"]
	izbira = form["izvoz-2-izbira"]
	if izbira == '':
		r.RESPONSE.redirect('/nadomescanja') 
	if izbira == 'oddo':
		od = form["od"]
		do = form["do"]	
		if not (od and do):
			r.RESPONSE.redirect('/nadomescanja') 
except:
	izvoz2 = False
	oseba = False



if izvoz1:
	mode = izvoz1
elif izvoz2:
	mode = izbira
else:
	r.RESPONSE.redirect('/nadomescanja') 


if mode == 'teden':
	first_day = DateTime() - DateTime().dow() - 7
	last_day = DateTime() + (7 - DateTime().dow()) - 7		
elif mode == 'tedenplus2':
	first_day = DateTime() - DateTime().dow() 
	last_day = first_day + 14
elif mode == 'tekoci':
	first_day = DateTime('%s-%s-%s' % (DateTime().year(), DateTime().month(), '1'))
	last_day = DateTime('%s-%s-%s' % (DateTime().year(), DateTime().month() + 1, '1')) - 1
elif mode == 'pretekli':
	first_day = DateTime('%s-%s-%s' % (DateTime().year(), DateTime().month() - 1, '1'))
	last_day = DateTime('%s-%s-%s' % (DateTime().year(), DateTime().month(), '1')) - 1
elif mode == 'oddo':	
	first_day = DateTime(od.split('.')[2] + '-' + od.split('.')[1] + '-' + od.split('.')[0])
	last_day = DateTime(do.split('.')[2] + '-' + do.split('.')[1] + '-' + do.split('.')[0])



test = context.portal_catalog(portal_type = "dezurstvo")[0].getObject()
print test.excel_export(first_day, last_day, oseba)

return printed
