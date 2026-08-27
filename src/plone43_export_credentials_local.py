#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Export encoded PAS credentials for local transfer only.

SECURITY SENSITIVE: writes password hashes. Keep the output outside Git and
transfer it only to the migration host. Read-only against Plone 4.3.
"""
from __future__ import print_function

import json
import os
import sys

SITES = ('portal', 'dezurstva', 'kiestra', 'preiskave', 'nadomescanja')
SCRIPT = 'plone43_export_credentials_local.py'

try:
    text_type = unicode
except NameError:
    text_type = str


def text(value):
    if value is None:
        return None
    if isinstance(value, text_type):
        return value
    if isinstance(value, str):
        return value.decode('utf-8', 'replace')
    return text_type(value)


def parse_output(argv):
    values = list(argv)
    positions = [i for i, value in enumerate(values)
                 if os.path.basename(value) == SCRIPT]
    if not positions:
        raise SystemExit('Unexpected instance-run argv: %r' % values)
    args = values[positions[-1] + 1:]
    if len(args) == 1 and args[0].startswith('--output='):
        return os.path.abspath(args[0].split('=', 1)[1])
    if len(args) == 2 and args[0] == '--output':
        return os.path.abspath(args[1])
    raise SystemExit('Use --output=/plone/instance/src/export/credentials-local.json')


def run(app, output):
    payload = {'schema_version': 1, 'sites': []}
    for site_id in SITES:
        site = app.unrestrictedTraverse(site_id)
        manager = site.acl_users.get('source_users')
        if manager is None:
            raise SystemExit('%s: missing acl_users/source_users' % site_id)
        passwords = getattr(manager, '_user_passwords', None)
        if passwords is None:
            raise SystemExit('%s: source_users has no _user_passwords' % site_id)
        records = []
        for user_id in sorted(passwords.keys()):
            encoded = passwords[user_id]
            if not text(encoded).startswith('{SSHA}'):
                raise SystemExit('%s/%s: unsupported credential scheme' %
                                 (site_id, user_id))
            records.append({'id': text(user_id), 'encoded_password': text(encoded)})
        payload['sites'].append({'id': site_id, 'credentials': records})
        print('%s: %d encoded credentials exported' % (site_id, len(records)))

    parent = os.path.dirname(output)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if isinstance(rendered, text_type):
        rendered = rendered.encode('utf-8')
    with open(output, 'wb') as handle:
        handle.write(rendered)
    try:
        os.chmod(output, 0o600)
    except Exception:
        pass
    print('Sensitive credential export: %s' % output)
    print('DO NOT COMMIT OR SHARE THIS FILE.')


if 'app' not in globals():
    raise SystemExit('Run with bin/instance run inside the Plone 4.3 buildout.')
run(app, parse_output(sys.argv))
