from django.core.management.base import BaseCommand
import dropbox
from django.conf import settings

import datetime
from django.utils import timezone

database_path = "/database/"
if hasattr(settings, 'SIMPLE_BACKUPS_DROPBOX_DATABASE_PATH'):
    database_path = settings.SIMPLE_BACKUPS_DROPBOX_DATABASE_PATH

DROPBOX_RENAME_DATE_FORMAT = "%c"
if hasattr(settings, 'SIMPLE_BACKUPS_DROPBOX_RENAME_DATE_FORMAT'):
    DROPBOX_RENAME_DATE_FORMAT = settings.SIMPLE_BACKUPS_DROPBOX_RENAME_DATE_FORMAT

def get_file_name():
    now = timezone.now()
    x = datetime.datetime(year=now.year,month=now.month,day=now.day,
                          hour=now.hour,minute=now.minute,second=now.second,microsecond=now.microsecond)

    formatted_date = x.strftime(DROPBOX_RENAME_DATE_FORMAT)
    return formatted_date + " | db.sqlite3"



class Command(BaseCommand):
    help = 'backs up sqlite file to dropbox' \
           'run this as a cron job as often as you want a backup of your db'

    def handle(self, *args, **options):

        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            database_upload_path = database_path + get_file_name()

            # database file with full path
            upload_file_path = settings.DATABASES['default']['NAME']


            # login to drop box dropbox
            client = dropbox.Dropbox(app_key = settings.SIMPLE_BACKUPS_DROPBOX_APP_KEY,
                                     app_secret = settings.SIMPLE_BACKUPS_APP_SECRET,
                                     oauth2_refresh_token = settings.SIMPLE_BACKUPS_DROPBOX_REFRESH_TOKEN
                                     )

            # upload file
            client.files_upload(open(upload_file_path, "rb").read(), database_upload_path)
            print("[SUCCESS] database uploaded to dropbox")

        else:
            raise Exception("backing up the database only supports sqlite databases")
