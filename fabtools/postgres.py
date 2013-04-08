"""
PostgreSQL users and databases
==============================

This module provides tools for creating PostgreSQL users and databases.

"""
from __future__ import with_statement

import re
import datetime
from fabric.api import cd, hide, settings, sudo


def _run_as_pg(command):
    """
    Run command as 'postgres' user
    """
    with cd('/var/lib/postgresql'):
        return sudo('sudo -u postgres %s' % command)


def _show(name):
    """
    Show PostgreSQL setting
    """
    regex = re.compile("\-+.*\n\s*([^\s]*)\s*\n.*", re.MULTILINE)
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        return regex.findall(_run_as_pg('psql -c "SHOW %s"' % name))[0]


def user_exists(name):
    """
    Check if a PostgreSQL user exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = _run_as_pg('''psql -t -A -c "SELECT COUNT(*) FROM pg_user WHERE usename = '%(name)s';"''' % locals())
    return (res == "1")


def create_user(name, password, superuser=False, createdb=False,
                createrole=False, inherit=True, login=True,
                connection_limit=None, encrypted_password=False):
    """
    Create a PostgreSQL user.

    Example::

        import fabtools

        # Create DB user if it does not exist
        if not fabtools.postgres.user_exists('dbuser'):
            fabtools.postgres.create_user('dbuser', password='somerandomstring')

        # Create DB user with custom options
        fabtools.postgres.create_user('dbuser2', password='s3cr3t',
            createdb=True, createrole=True, connection_limit=20)

    """
    options = [
        'SUPERUSER' if superuser else 'NOSUPERUSER',
        'CREATEDB' if createdb else 'NOCREATEDB',
        'CREATEROLE' if createrole else 'NOCREATEROLE',
        'INHERIT' if inherit else 'NOINHERIT',
        'LOGIN' if login else 'NOLOGIN',
    ]
    if connection_limit is not None:
        options.append('CONNECTION LIMIT %d' % connection_limit)
    password_type = 'ENCRYPTED' if encrypted_password else 'UNENCRYPTED'
    options.append("%s PASSWORD '%s'" % (password_type, password))
    options = ' '.join(options)
    _run_as_pg('''psql -c "CREATE USER %(name)s %(options)s;"''' % locals())


def database_exists(name):
    """
    Check if a PostgreSQL database exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'),
                  warn_only=True):
        return _run_as_pg('''psql -d %(name)s -c ""''' % locals()).succeeded


def create_database(name, owner, template='template0', encoding='UTF8',
                    locale='en_US.UTF-8'):
    """
    Create a PostgreSQL database.

    Example::

        import fabtools

        # Create DB if it does not exist
        if not fabtools.postgres.database_exists('myapp'):
            fabtools.postgres.create_database('myapp', owner='dbuser')

    """
    _run_as_pg('''createdb --owner %(owner)s --template %(template)s \
                  --encoding=%(encoding)s --lc-ctype=%(locale)s \
                  --lc-collate=%(locale)s %(name)s''' % locals())


def drop_database(name):
    _run_as_pg('''dropdb %(name)s''' % locals())


def export_database(name, filename=None):
    _run_as_pg("""pg_dump %s -f %s""" % (
        name, filename or datetime.datetime.now().strftime('%Y-%m-%d_%H:%M_' + name + '.sql')
    ))


def import_database(name, filename):
    _run_as_pg("""psql -d %(name)s -a -f %(filename)s""" % locals())


def create_schema(name, database, owner=None):
    """
    Create a schema within a database.
    """
    if owner:
        _run_as_pg('''psql %(database)s -c "CREATE SCHEMA %(name)s AUTHORIZATION %(owner)s"''' % locals())
    else:
        _run_as_pg('''psql %(database)s -c "CREATE SCHEMA %(name)s"''' % locals())
