import os,sys,re
import datetime as dt
from fabric.api import *
from fabric.context_managers import hide

env.hosts = ['www']
env.root_dir = "/home/httpd"
env.projects = [ 'comics', 'chicks', 'redpics', 'earthporn', 'devgrabber' ]

def proj_path( proj ):
    return os.path.join( env.root_dir, proj )

@task
def pil():
    local( 'pip install --allow-external PIL --allow-unverified PIL PIL==1.1.7' )

@task
def mass_push():
    for project in env.projects:
        with lcd( proj_path( project ) ):
            local("hg push")

@task
def mass_update():
    for project in env.projects:
        with lcd( proj_path( project ) ):
            local("hg pull")
            local("hg onsub 'hg pull --update'")

@task
def mass_commit( msg ):
    for project in env.projects:
        with lcd( os.path.join( env.root_dir, project ) ):
            local("hg commit -m '%s'" % msg )


@task
def copy( rel_path ):
    with settings( warn_only = True ):
        for project in env.projects:
            res = local( "cp -rvf %s %s" % ( rel_path, os.path.join( proj_path( project ), rel_path ) ) )
            if res.failed: continue

@task
def freeze():
    local( "pip freeze -r requirements.txt > requirements.txt" )

@task
def updatedb( app = None):
    if not app:
        app = "devgrabber"

    with settings(hide('warnings'), warn_only=True ):
        result = local( "./manage.py schemamigration --auto %s" % app )

    if not result.failed:
        local( "./manage.py migrate" )

@task
def coverage( app = None ):
    if app is None:
        app = 'backend'

    local( "coverage run --source='%s' manage.py test %s" % (app,app) )
    local( "coverage report" )

@task
def collect():
    local( "./manage.py collectstatic --noinput" )

@task
def server():
    collect()
    local( "./manage.py runserver_plus 0.0.0.0:9000")

@task
def shell():
    local( "./manage.py shell_plus" )

@task
def worker():
    local( "./manage.py celeryd worker --loglevel=DEBUG" )

@task
def mkvirtualenv():
    local( "virtualenvwrapper --no-site-packages virt" )
    local( "pip install -r requirements.txt --no-install" )
    local( "pip install -r requirements.txt --no-download" )

@task
def reindex():
    local( "./manage.py rebuild_index --noinput -v2" )

@task
def bounce():
    for project in env.projects:
        run( "touch %s/%s" % (env.root_dir,project) )

@task
def rmtoday(project='devgrabber'):
    fmt = "%Y-%m-%d"
    date = dt.datetime.now().strftime( fmt )

    sudo( "rm -rf /home/httpd/dailypics/{project}/{date}".format(project=project,date=date) )
    sudo( "rm -rf /home/httpd/dailypics/{project}/cache/{date}".format(project=project,date=date) )
    sudo( "rm -f /home/httpd/{project}/*.log".format(project=project,date=date) )
