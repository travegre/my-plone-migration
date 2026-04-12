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
ime = form['ime-in-priimek']
subject = form['topic']
zahtevek = form['comments']

mailhost = getToolByName(context, 'MailHost')
#mh.send(messageText, mto=None, mfrom=None, 
#      subject=None, encode=None, 
#      immediate=False, charset='utf8', msg_type=None)
#mailhost=getattr(context, context.superValues('Mail Host')[0].id)

mMsg = 'Spoštovani,\n\noseba\n\n'
mMsg += ime
mMsg += '\n\nje poslala naslednjo zahtevo:\n\n'
mMsg += zahtevek

mTo = 'damijan@hruska.si'
mFrom = 'info@imi.si'
mSubj = 'Zahtevek osebe ' + ime + ' za spremembo dežurstva.'

mailhost.send(mMsg, mTo, mFrom, mSubj)

r.RESPONSE.redirect('/dezurstva/?poslano=1')
return printed    
