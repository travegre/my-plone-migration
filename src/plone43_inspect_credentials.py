#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Inspect Plone 4.3 PAS credential storage without exporting credentials.

Read-only.  Reports user-source/authentication plugin classes and, where the
standard ZODBUserManager exposes stored passwords, only the encoding prefix
(e.g. ``{SSHA}``) -- never the encoded password itself.

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
    # Some older encodings do not use a brace prefix.  Do not print any value.
    return '<unprefixed>'


def plugin_ids(pas, interface_name):
    try:
        from Products.PluggableAuthService import interfaces
        iface = getattr(interfaces, interface_name)
        return list(pas.plugins.listPluginIds(iface))
    except Exception:
        return []


def inspect_site(site_id, site):
    pas = site.acl_users
    print('\n[%s]' % site_id)
    print('PAS: %s' % dotted(pas))

    for interface_name in ('IUserEnumerationPlugin', 'IUserAdderPlugin',
                           'IAuthenticationPlugin', 'IPropertiesPlugin',
                           'IGroupsPlugin'):
        ids = plugin_ids(pas, interface_name)
        if ids:
            print('%s: %s' % (interface_name, ', '.join(ids)))
            for plugin_id in ids:
                try:
                    plugin = pas[plugin_id]
                    print('  %s -> %s' % (plugin_id, dotted(plugin)))
                except Exception:
                    pass

    # Standard PAS ZODBUserManager stores encoded passwords in
    # ``_user_passwords``.  Only aggregate the encoding schemes.
    found = False
    for plugin_id in pas.objectIds():
        try:
            plugin = pas[plugin_id]
        except Exception:
            continue
        passwords = getattr(plugin, '_user_passwords', None)
        if not isinstance(passwords, dict):
            continue
        found = True
        counts = {}
        for encoded in passwords.values():
            name = scheme(encoded)
            counts[name] = counts.get(name, 0) + 1
        rendered = ', '.join('%s=%d' % item for item in sorted(counts.items()))
        print('credential store %s (%s): %d users; schemes: %s' %
              (plugin_id, dotted(plugin), len(passwords), rendered or '<empty>'))
    if not found:
        print('credential store: no standard _user_passwords mapping found')


def run(app):
    for site_id in SITES:
        inspect_site(site_id, app.unrestrictedTraverse(site_id))
    print('\nNo password hashes or SMTP passwords were printed.')


if 'app' not in globals():
    raise SystemExit('Run with bin/instance run inside the Plone 4.3 buildout.')
run(app)
