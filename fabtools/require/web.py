from fabric.api import env, cd
from fabtools.require.files import directory, configs as _configs
from fabtools.utils import run_as_root


def configs(filenames, **kw):

    def callback():
        lib_tarball = 'lib.tar.gz'
        directory(env.web['lib_root'], group='admin', mode='755', use_sudo=True)
        with cd('%s/..' % env.web['lib_root']):
            run_as_root('wget --no-check-cert %s -O %s -nv' % (env.web['lib_source'], lib_tarball))
            run_as_root('tar -xzvf %s' % lib_tarball)

    _configs(filenames, callback, **kw)


def config(filename, *args, **kw):
    configs([filename], *args, **kw)
