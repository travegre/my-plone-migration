# -*- coding: utf-8 -*-
import json
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class NadomescanjaDataView(BrowserView):

    def __call__(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        labs      = self._get_labs(portal)
        zaposleni = self._get_zaposleni(portal)

        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(
            {'laboratoriji': labs, 'zaposleni': zaposleni},
            ensure_ascii=False
        )

    def _get_labs(self, portal):
        try:
            folder = portal.unrestrictedTraverse('laboratoriji')
        except Exception as e:
            return [{'error': 'laboratoriji folder not found: ' + str(e)}]

        result = []
        for obj in folder.objectValues():
            try:
                if getattr(obj, 'portal_type', None) != 'laboratorij':
                    continue

                # handle both StringField (str) and old LinesField (tuple/list)
                vodja_id = obj.getPrivzeti_vodja() or ''
                if isinstance(vodja_id, (list, tuple)):
                    vodja_id = vodja_id[0] if vodja_id else ''
                vodja_id = str(vodja_id).strip()

                vodja_naziv = u''
                if vodja_id:
                    try:
                        vodja_obj   = portal.unrestrictedTraverse(
                            'dezurstva/seznam_zaposlenih/' + vodja_id
                        )
                        vodja_naziv = vodja_obj.Title()
                        if isinstance(vodja_naziv, str):
                            vodja_naziv = vodja_naziv.decode('utf-8')
                    except Exception:
                        vodja_naziv = vodja_id.decode('utf-8') \
                                      if isinstance(vodja_id, str) else unicode(vodja_id)

                naziv = obj.Title()
                if isinstance(naziv, str):
                    naziv = naziv.decode('utf-8')

                result.append({
                    'id':          obj.getId(),
                    'naziv':       naziv,
                    'okrajsava':   obj.getOkrajsava() or '',   # add this
                    'vodja_id':    vodja_id,
                    'vodja_naziv': vodja_naziv
                })
            except Exception:
                continue
        return result


    def _get_zaposleni(self, portal):
        try:
            folder = portal.unrestrictedTraverse('dezurstva/seznam_zaposlenih')
        except Exception as e:
            return [{'error': 'seznam_zaposlenih folder not found: ' + str(e)}]

        result = []
        for obj in folder.objectValues():
            try:
                obj_id = obj.getId()
                if not obj_id:
                    continue
                if obj.getExcludeFromNav():
                    continue
                naziv = obj.Title()
                if isinstance(naziv, str):
                    naziv = naziv.decode('utf-8')
                result.append({'id': obj_id, 'naziv': naziv})
            except Exception:
                continue
        return result