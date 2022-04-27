django-simple-backups
-

## Introduction
This django app gives you a simple management command to backup your sqlite database and media files to dropbox.
This was created because had countless errors for me and it was easier to just create a new package. All contributions are welcome. 
Please note currently this app will not delete old backups. if you want to delete backups then you have to go to dropbox and do it yourself.

## Installation

    pip install django-simple-backups

Add `backups` to your Django settings INSTALLED_APPS:

    INSTALLED_APPS = [
        # ...
        "backups",
    ]

### Settings
    # other required settings

    # must use default database and must use 'ENGINE': 'django.db.backends.sqlite3'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            ...
        }
    }

    # must have MEDIA_ROOT
    # must be to absolute path
    
    MEDIA_ROOT = BASE_DIR / 'somepath'

    # simple backups settings
    # must have access token
    SIMPLE_BACKUPS_DROPBOX_ACCESS_TOKEN = "put your drop box access token here"

    # folder in drop box to save all database files to default is "/database/"
    SIMPLE_BACKUPS_DROPBOX_DATABASE_PATH = "/database/"
    # folder in drop box to save all media folders to. | for each backup a folder with todays date will be added your website media files will get added to that folder
    # default is "/media/"
    SIMPLE_BACKUPS_DROPBOX_MEDIA_PATH = "/media/"

    # format of the date that the backups will use to rename
    # see for date codes https://www.w3schools.com/python/gloss_python_date_format_codes.asp
    # default is "%c" - Mon Dec 31 17:41:00 2018
    SIMPLE_BACKUPS_DROPBOX_RENAME_DATE_FORMAT = "%c"

## Management commands

### manage.py backupmedia 
creates a new folder in dropbox with the current date as the name of the folder. 
For example if your media folder structure looks like:

    media
    |   file one
    |   file two
    |   documents
    |   |   document one

then your uploaded dropbox folder will look like

    SIMPLE_BACKUPS_DROPBOX_MEDIA_PATH/current_date media backup
    |   file one
    |   file two
    |   documents
    |   |   document one
### manage.py backupdatabase
* copies your database
* uploads to dropbox at `SIMPLE_BACKUPS_DROPBOX_DATABASE_PATH/current_date | db.sqlite3`

