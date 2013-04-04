from __future__ import with_statement

from fabric.api import run, env, settings, hide
from fabtools.utils import run_as_root


def migrate_schema(use_sudo=False, **kw):
    func = use_sudo and run_as_root or run
    func('python manage.py syncdb --all')
    for app in env.django['south_apps']:
        with settings(hide('warnings'), warn_only=True):
            if func('python manage.py schemamigration %s --auto' % app).succeeded:
                func('python manage.py migrate %s' % app)
