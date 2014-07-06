"""
Common tools for deploy run shell and the like.
"""

import os
from string import Template
from urllib import urlencode

from fabric.api import *
from fabric.colors import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists

env.use_ssh_config = True


@task
def pep8():
    """Run Pep8"""
    local("pep8 dtrove --exclude='*migrations*','*static*'")


@task
def test(skip_js='False'):
    """Run the test suite"""
    local("coverage run --include='dtrove*' --omit='*migration*' manage.py test dtrove")
    if skip_js == 'False':
        pass
        # TODO: (rmyers): if we include js then handle that here
        #with lcd('assets'):
            #local('node_modules/grunt-cli/bin/grunt jasmine')
    pep8()


@task
def docs():
    """Build the docs"""
    with lcd('docs'):
        local('make html')


@task
def install():
    """Install the node_modules dependencies"""
    local('git submodule update --init')
    if not os.path.isfile('july/secrets.py'):
        local('cp july/secrets.py.template july/secrets.py')

    local('python manage.py syncdb')
    local('python manage.py migrate')
    local('python manage.py loaddata july/fixtures/development.json')

    with lcd('assets'), settings(warn_only=True):
        out = local('npm install')
        if out.failed:
            print(red("Problem running npm, did you install node?"))


@task
def watch():
    """Grunt watch development files"""
    with lcd('assets'):
        local('node_modules/grunt-cli/bin/grunt concat less:dev watch')


@task
def compile():
    """Compile assets for production."""
    with lcd('assets'):
        local('node_modules/grunt-cli/bin/grunt less:prod uglify')
