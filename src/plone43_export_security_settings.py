#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Export Plone 4.3 users/groups/roles and compatible site settings.

Read-only.  Run with the old instance stopped::

    bin/instance run src/plone43_export_security_settings.py \
        --output-dir=/plone/instance/src/export

Passwords are intentionally NOT exported by this file.  They require a
separate credential-migration decision because PAS password storage is plugin
specific and must never be committed to Git.
"""
from __future__ import print_function

import json
import os
import sys

SITES = ('portal', 'dezurstva', 'kiestra', 'preiskave', 'nadomescanja')
SCRIPT = 'plone43_export_security_settings.py'

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
    try:
        return text_type(value)
    except Exception:
        return text_type(repr(value), 'utf-8', 'replace')


def scalar(value):
    if value is None or isinstance(value, (bool, int, long, float)):
        return value
    if isinstance(value, (list, tuple, set)):
        return [scalar(v) for v in value]
    if isinstance(value, dict):
        return dict((text(k), scalar(v)) for k, v in value.items())
    return text(value)


def parse_output_dir(argv):
    values = list(argv)
    positions = [i for i, value in enumerate(values)
                 if os.path.basename(value) == SCRIPT]
    if not positions:
        raise SystemExit('Unexpected instance-run argv: %r' % values)
    args = values[positions[-1] + 1:]
    if len(args) == 1 and args[0].startswith('--output-dir='):
        return os.path.abspath(args[0].split('=', 1)[1])
    if len(args) == 2 and args[0] == '--output-dir':
        return os.path.abspath(args[1])
    raise SystemExit('Use --output-dir=/plone/instance/src/export')


def member_record(site, member):
    user_id = text(member.getId())
    props = {}
    for name in ('fullname', 'email', 'description', 'location', 'home_page'):
        try:
            props[name] = scalar(member.getProperty(name, ''))
        except Exception:
            pass
    roles = []
    try:
        roles = [text(r) for r in member.getRoles() if r not in ('Authenticated',)]
    except Exception:
        pass
    groups = []
    try:
        groups = [text(g.getGroupId()) for g in site.portal_groups.getGroupsByUserId(user_id)]
    except Exception:
        pass
    return {
        'id': user_id,
        'properties': props,
        'roles': roles,
        'groups': groups,
    }


def users(site):
    result = []
    seen = set()
    try:
        members = site.portal_membership.listMembers()
    except Exception:
        members = []
    for member in members:
        try:
            user_id = text(member.getId())
        except Exception:
            continue
        if not user_id or user_id in seen:
            continue
        seen.add(user_id)
        result.append(member_record(site, member))
    result.sort(key=lambda item: item['id'])
    return result


def groups(site):
    result = []
    try:
        wrapped = site.portal_groups.listGroups()
    except Exception:
        wrapped = []
    for group in wrapped:
        try:
            group_id = text(group.getGroupId())
        except Exception:
            continue
        item = {'id': group_id, 'title': group_id, 'description': '',
                'roles': [], 'members': []}
        for attr, target in (('getGroupTitleOrName', 'title'),
                             ('getGroupDescription', 'description')):
            try:
                item[target] = text(getattr(group, attr)())
            except Exception:
                pass
        try:
            item['roles'] = [text(r) for r in group.getRoles()
                             if r not in ('Authenticated',)]
        except Exception:
            pass
        try:
            item['members'] = sorted(text(m.getId()) for m in group.getGroupMembers())
        except Exception:
            pass
        result.append(item)
    result.sort(key=lambda item: item['id'])
    return result


def local_roles(obj):
    try:
        return [[text(p), [text(r) for r in roles]]
                for p, roles in obj.get_local_roles()]
    except Exception:
        return []


def site_properties(site):
    result = {}
    props = getattr(site, 'portal_properties', None)
    sheet = getattr(props, 'site_properties', None) if props is not None else None
    if sheet is None:
        return result
    # Explicitly selected settings with useful Plone-5 equivalents or
    # diagnostic value.  Do not blindly transplant the whole 4.3 sheet.
    names = (
        'email_from_address', 'email_from_name', 'default_language',
        'enable_livesearch', 'enable_sitemap', 'exposeDCMetaTags',
        'many_groups', 'default_page', 'disable_folder_sections',
        'types_not_searched', 'use_email_as_login',
    )
    for name in names:
        try:
            if sheet.hasProperty(name):
                result[name] = scalar(sheet.getProperty(name))
        except Exception:
            pass
    return result


def mailhost(site):
    mh = getattr(site, 'MailHost', None)
    if mh is None:
        return None
    result = {}
    for name in ('smtp_host', 'smtp_port', 'smtp_uid'):
        try:
            result[name] = scalar(getattr(mh, name))
        except Exception:
            pass
    # Password deliberately omitted.  Record whether one appears configured.
    try:
        result['smtp_password_configured'] = bool(getattr(mh, 'smtp_pwd', None))
    except Exception:
        result['smtp_password_configured'] = None
    return result


def workflow_chains(site):
    result = {}
    wf = getattr(site, 'portal_workflow', None)
    types = getattr(site, 'portal_types', None)
    if wf is None or types is None:
        return result
    for type_id in types.objectIds():
        try:
            chain = list(wf.getChainForPortalType(type_id) or ())
            if chain:
                result[text(type_id)] = [text(x) for x in chain]
        except Exception:
            pass
    return result


def site_record(site, site_id):
    return {
        'id': site_id,
        'title': text(site.Title()),
        'description': text(site.Description()),
        'users': users(site),
        'groups': groups(site),
        'site_local_roles': local_roles(site),
        'properties': site_properties(site),
        'mailhost': mailhost(site),
        'workflow_chains': workflow_chains(site),
        'passwords_exported': False,
    }


def run(app, outdir):
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    payload = {
        'schema_version': 1,
        'source': 'Plone 4.3',
        'passwords_exported': False,
        'sites': [],
    }
    for site_id in SITES:
        site = app.unrestrictedTraverse(site_id)
        record = site_record(site, site_id)
        payload['sites'].append(record)
        print('%s: %d users, %d groups' %
              (site_id, len(record['users']), len(record['groups'])))

    path = os.path.join(outdir, 'security-settings.json')
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if isinstance(rendered, text_type):
        rendered = rendered.encode('utf-8')
    with open(path, 'wb') as handle:
        handle.write(rendered)
    print('Security/settings export: %s' % path)
    print('Passwords: NOT exported; SMTP password: NOT exported')


if 'app' not in globals():
    raise SystemExit('Run with bin/instance run inside the Plone 4.3 buildout.')
run(app, parse_output_dir(sys.argv))
