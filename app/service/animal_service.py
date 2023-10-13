from flask import jsonify
from flask_restful import Resource
from app.model.animal import AnimalType
import os
import nextcloud_client
from datetime import datetime
from flask import current_app as app


class AnimalTypeList(Resource):
    @staticmethod
    def get():
        if 'NEXTCLOUD_HOST' in os.environ and 'NEXTCLOUD_USER' in os.environ and 'NEXTCLOUD_PASSWORD' in os.environ:
            nc = nextcloud_client.Client(os.environ.get('NEXTCLOUD_HOST'))
            nc.login(os.environ.get('NEXTCLOUD_USER'), os.environ.get('NEXTCLOUD_PASSWORD'))

            backup_dir = 'farminv-backup-server'
            try:
                for element in nc.list(backup_dir):
                    app.logger.debug(element.path)
            except:
                app.logger.warning('backup directory on NEXTCLOUD does not exist creating...')
                nc.mkdir(backup_dir)
            for dir_path, dir_names, filenames in os.walk("/"):
                for filename in [f for f in filenames if f.endswith("inv.db")]:
                    # normal path : /usr/local/var/app.app-instance/farminv.db
                    nc.put_file(f'{backup_dir}/{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}_backup.db',
                                os.path.join(dir_path, filename))

        else:
            app.logger.warning('Environment variables for backup on nextcloud not set')
        return jsonify([animal_type.name for animal_type in AnimalType])
