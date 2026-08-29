#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read-only catalog index/column inventory for the five Plone 4.3 sites."""
from __future__ import print_function

SITES = ('portal', 'dezurstva', 'kiestra', 'preiskave', 'nadomescanja')


def dotted(obj):
    return '%s.%s' % (obj.__class__.__module__, obj.__class__.__name__)


def safe_value(obj, name):
    try:
        value = getattr(obj, name)
        return value() if callable(value) else value
    except Exception as exc:
        return '<error: %r>' % (exc,)


def run(app):
    for site_id in SITES:
        print('\n' + '=' * 78)
        print('SITE:', site_id)
        try:
            site = app.unrestrictedTraverse(site_id)
            catalog = site.portal_catalog
        except Exception as exc:
            print('ERROR:', repr(exc))
            continue

        indexes = catalog._catalog.indexes
        print('INDEX COUNT:', len(indexes))
        for name in sorted(indexes):
            index = indexes[name]
            print('INDEX\t%s\t%s' % (name, dotted(index)))
            for attr in ('getIndexSourceNames', 'getLexicon', 'lexicon_id',
                         '_indexed_attrs', 'indexed_attrs'):
                if hasattr(index, attr):
                    print('  %s = %r' % (attr, safe_value(index, attr)))
            lexicon_id = getattr(index, 'lexicon_id', None)
            if lexicon_id:
                try:
                    lexicon = getattr(catalog, lexicon_id)
                except Exception:
                    try:
                        lexicon = getattr(site, lexicon_id)
                    except Exception:
                        lexicon = None
                if lexicon is not None:
                    pipeline = getattr(lexicon, '_pipeline', None)
                    if pipeline is not None:
                        print('  lexicon pipeline = %r' %
                              [dotted(item) for item in pipeline])

        schema = getattr(catalog._catalog, 'schema', {})
        try:
            columns = sorted(schema.keys())
        except Exception:
            columns = sorted(schema)
        print('COLUMNS:', repr(columns))


if 'app' not in globals():
    raise SystemExit('Run with bin/instance run inside the Plone 4.3 buildout.')
run(app)
