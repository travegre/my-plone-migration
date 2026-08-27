#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Inspect Plone 4.3 PAS credential storage without exporting credentials.

Read-only. Reports PAS plugin classes and, where a plugin exposes a password
mapping such as ZODBUserManager ``_user_passwords``, only aggregate encoding
prefixes (e.g. ``{SSHA}``) -- never usernames, hashes, or passwords.

Run::

    bin/instance run src/plone43_inspect_credentials.py
"""
from __future__ import print_function

import re

SITES = ('portal', 'dezurstva', 'kiestra', 'preiskave', 'nadomescanja')


def dotted(obj):
    cls = obj.__class__
    return '%s.%s' % (cls.__module__, cls.__name__)


def scheme(value):
    if value is None:
        return '<none>'
    try:
        if not isinstance(value, basestring):
            value = str(value)
    except NameError:
        value = str(value)
    match = re.match(r'^(\{[^}]+\})', value)
    if match:
        return match.group(1)
    return '<unprefixed>'


def mapping_values(value):
    """Return values from dict/PersistentMapping/BTrees without assuming dict."""
    if value is None:
        return None
    values = getattr(value, 'values', None)
    if callable(values):
        try:
            return list(values())
        except Exception:
            pass
    items = getattr(value, 'items', None)
    if callable(items):
        try:
            return [item[1] for item in items()]
        except Exception:
            pass
    return None


def plugin_ids(pas, interface_name):
    # PAS interface locations vary a little across old versions. Try both.
    candidates = []
    try:
        from Products.PluggableAuthService import interfaces
        candidates.append(getattr(interfaces, interface_name, None))
    except Exception:
        pass
    try:
        module = __import__(
            'Products.PluggableAuthService.interfaces.plugins',
            fromlist=[interface_name])
        candidates.append(getattr(module, interface_name, None))
    except Exception:
        pass
    for iface in candidates:
        if iface is None:
            continue
        try:
            ids = list(pas.plugins.listPluginIds(iface))
            if ids:
                return ids
        except Exception:
            pass
    return []


def inspect_site(site_id, site):
    pas = site.acl_users
    print('\n[%s]' % site_id)
    print('PAS: %s' % dotted(pas))

    print('contained plugins:')
    for plugin_id in pas.objectIds():
        try:
            plugin = pas[plugin_id]
            print('  %s -> %s' % (plugin_id, dotted(plugin)))
        except Exception:
            pass

    for interface_name in ('IUserEnumerationPlugin', 'IUserAdderPlugin',
                           'IAuthenticationPlugin', 'IPropertiesPlugin',
                           'IGroupsPlugin'):
        ids = plugin_ids(pas, interface_name)
        if ids:
            print('%s active: %s' % (interface_name, ', '.join(ids)))

    found = False
    for plugin_id in pas.objectIds():
        try:
            plugin = pas[plugin_id]
        except Exception:
            continue
        for attr in ('_user_passwords', '_passwords'):
            try:
                store = getattr(plugin, attr, None)
            except Exception:
                store = None
            values = mapping_values(store)
            if values is None:
                continue
            found = True
            counts = {}
            for encoded in values:
                name = scheme(encoded)
                counts[name] = counts.get(name, 0) + 1
            rendered = ', '.join('%s=%d' % item for item in sorted(counts.items()))
            print('credential store %s.%s (%s): %d users; schemes: %s' %
                  (plugin_id, attr, dotted(plugin), len(values),
                   rendered or '<empty>'))

    if not found:
        print('credential store: no password mapping found on contained plugins')


def run(app):
    for site_id in SITES:
        inspect_site(site_id, app.unrestrictedTraverse(site_id))
    print('\nNo usernames, password hashes, passwords, or SMTP passwords were printed.')


if 'app' not in globals():
    raise SystemExit('Run with bin/instance run inside the Plone 4.3 buildout.')
run(app)
