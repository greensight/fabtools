from fabric.api import env
from fabtools.require.files import remove, configs as _configs
from fabtools.require.service import restarted


APACHE_LOG_DIR = '/var/log/apache2'
DJANGO_DIR = '/usr/local/lib/python2.7/dist-packages/django'


def _service_name(version=None):
    return 'apache2'


def _config_dir():
    return '/etc/apache2/sites-enabled'


def configs(filenames, **kw):

    def callback():
        remove('%s/000-default' % _config_dir(), use_sudo=True)
        restarted(_service_name())

    env.web.update({
        'server_log_dir': APACHE_LOG_DIR,
        'django_dir': DJANGO_DIR
    })
    _configs(
        filenames,
        callback,
        config_dir=_config_dir(),
        use_sudo=True,
        **kw
    )


def config(filename, *args, **kw):
    configs([filename], *args, **kw)
