from __future__ import with_statement

from fabric.api import run, env, settings, hide
from fabtools.utils import run_as_root


def migrate_schema(use_sudo=False, **kw):
    func = use_sudo and run_as_root or run
    func('python manage.py syncdb')
    for app in env.django['south_apps']:
        func('python manage.py migrate %s --no-initial-data' % app)
    func('python manage.py migrate --all --no-initial-data')
