from fabric.api import env, cd
from fabtools.require.files import link, remove, configs as _configs
from fabtools.require.service import restarted


APACHE_CONFIG_DIR = '/etc/apache2'
APACHE_LOG_DIR = '/var/log/apache2'
DJANGO_DIR = '/usr/local/lib/python2.7/dist-packages/django'


def _service_name(version=None):
    return 'apache2'


def configs(filenames, **kw):

    def callback():
        config_file_path = '%s%s' % (env.cwd, 'site.conf')
        with cd(APACHE_CONFIG_DIR + '/sites-enabled'):
            remove('000-default', use_sudo=True)
            link(config_file_path, env.ws['name'], use_sudo=True)
        restarted(_service_name())

    env.ws.update({
        'config_dir': APACHE_CONFIG_DIR,
        'log_dir': APACHE_LOG_DIR,
        'django_dir': DJANGO_DIR
    })
    _configs(filenames, callback, **kw)
