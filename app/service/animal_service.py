from flask import jsonify
from flask_restful import Resource
from app.model.animal import AnimalType
import os
import nextcloud_client
from datetime import datetime


class AnimalTypeList(Resource):
    @staticmethod
    def get():
        if 'NEXTCLOUD_HOST' in os.environ and 'NEXTCLOUD_USER' in os.environ and 'NEXTCLOUD_PASSWORD' in os.environ:
            nc = nextcloud_client.Client(os.environ.get('NEXTCLOUD_HOST'))
            nc.login(os.environ.get('NEXTCLOUD_USER'), os.environ.get('NEXTCLOUD_PASSWORD'))

            backup_dir = 'farminv-backup'
            try:
                for element in nc.list(backup_dir):
                    print(element.path)
            except:
                nc.mkdir(backup_dir)
            nc.put_file(f'{backup_dir}/{datetime.now().strftime("%Y_%m_%d_%H-%M-%S")}_backup.db',
                        '../instance/farminv.db')
            # logger.info('check animals')
        else:
            print('Environment variables for backup on nextcloud not set')
        return jsonify([animal_type.name for animal_type in AnimalType])
