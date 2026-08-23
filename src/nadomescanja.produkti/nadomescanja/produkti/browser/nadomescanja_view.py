# -*- coding: utf-8 -*-
# nadomescanja_view.py — can be just this now
import json
from Products.Five import BrowserView

class NadomescanjaView(BrowserView):
    def rows(self):
        raw = self.context.getNadomescanja_json() or '[]'
        try:    return json.loads(raw)
        except: return []
