import os

from django.core.management.base import BaseCommand
import dropbox
from django.conf import settings
import datetime
from django.utils import timezone


dropbox_media_path = "/media/"
if hasattr(settings, 'SIMPLE_BACKUPS_DROPBOX_MEDIA_PATH'):
    dropbox_media_path = settings.SIMPLE_BACKUPS_DROPBOX_MEDIA_PATH

DROPBOX_RENAME_DATE_FORMAT = "%c"
if hasattr(settings, 'SIMPLE_BACKUPS_DROPBOX_RENAME_DATE_FORMAT'):
    DROPBOX_RENAME_DATE_FORMAT = settings.SIMPLE_BACKUPS_DROPBOX_RENAME_DATE_FORMAT


def get_dir_name():
    now = timezone.now()
    x = datetime.datetime(year=now.year,month=now.month,day=now.day,
                          hour=now.hour,minute=now.minute,second=now.second,microsecond=now.microsecond)

    formatted_date = x.strftime(DROPBOX_RENAME_DATE_FORMAT)
    return formatted_date + "media backup"


class Command(BaseCommand):
    help = 'backs up media files to dropbox' \
           'run this as a cron job as often as you want a backup of your media files'

    def handle(self, *args, **options):

        if settings.MEDIA_ROOT:
            media_upload_path = os.path.join(dropbox_media_path , get_dir_name())

            # login to drop box dropbox
            # login to drop box dropbox
            client = dropbox.Dropbox(app_key = settings.SIMPLE_BACKUPS_DROPBOX_APP_KEY,
                                     app_secret = settings.SIMPLE_BACKUPS_APP_SECRET,
                                     oauth2_refresh_token = settings.SIMPLE_BACKUPS_DROPBOX_REFRESH_TOKEN
                                     )

            # upload files
            # enumerate local files recursively
            num_of_files = 0
            for root, dirs, files in os.walk(settings.MEDIA_ROOT):

                for filename in files:
                    # construct the full local path
                    local_path = os.path.join(root, filename)

                    # construct the full Dropbox path
                    relative_path = os.path.relpath(local_path, settings.MEDIA_ROOT)
                    dropbox_path = os.path.join(media_upload_path, relative_path)
                    # fix path with wrong \ instead of /
                    dropbox_path = dropbox_path.replace('\\', "/")

                    # upload the file
                    with open(local_path, 'rb') as f:
                        print("uploading",dropbox_path)
                        client.files_upload(f.read(), dropbox_path)
                        num_of_files += 1


            print(f"[SUCCESS] uploaded {num_of_files} files to dropbox")

        else:
            raise Exception("you must have a media root to backup media")
