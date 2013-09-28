import os

from fabric.api import cd, env, run
from fabric.colors import green
from fabric.contrib.files import exists
from fabric.utils import puts


env.hosts = ['production@gitality.com']

env.project_name = 'gitality'
env.project_db_name = env.project_name

env.project_home = '/srv/production/projects'
env.project_root_dirname = 'gitality.com'
env.project_root = '{0.project_home}/{0.project_root_dirname}'.format(env)

env.virtualenv_root = '{0}/{1.project_name}'.format(os.environ['WORKON_HOME'], env)
env.virtualenv_activate_command = 'source {.virtualenv_root}/bin/activate'.format(env)

env.site_down_file = '.down'
env.touch_reload_file = '.reload'

env.git_repository = 'git@github.com:dmrz/gitality.git'


def prun(command):
    """
    Runs command from project root directoy.
    """
    with cd(env.project_root):
        run(command)


def make(target):
    """
    Invokes Makefile target.
    """
    prun(target)


def supervisorctl(action, program='',  options=''):
    run('supervisorctl {0} {1} {2}'.format(action, options, program))


def site_down():
    prun('touch {}'.format(env.site_down_file))
    puts(green('Site is down for maintenance'))


def site_up():
    prun('rm {}'.format(env.site_down_file))
    puts(green('Site is up and running'))


def touch_reload():
    """
    uWSGI touch reload
    """
    prun('touch {}'.format(env.touch_reload_file))


def git_clone():
    with cd(env.project_home):
        if exists(env.project_root_dirname):
            run('rm -rf {.project_root_dirname}'.format(env))
        run('git clone -q {0.git_repository} {0.project_root_dirname}'.format(env))


def git_pull():
    prun('git pull -q')


def bootstrap():
    """
    Bootstraps project for the first time.
    """

    git_clone()

    make('bootstrap')
    make('settings_production')
    make('requirements')
    make('db_production')
    make('collectstatic')


def deploy():
    """
    Deploys updated project.
    """

    site_down()

    git_pull()

    make('syncdb')
    make('migrate')
    make('seed_production')
    make('collectstatic')

    touch_reload()

    site_up()
