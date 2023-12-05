import datetime
import logging

import nextcloud_client
import os


def get_latest_nc_backup():
    logging.info('start fetching backup')
    nc = nextcloud_client.Client(os.environ.get('NEXTCLOUD_HOST'))
    nc.login(os.environ.get('NEXTCLOUD_USER'), os.environ.get('NEXTCLOUD_PASSWORD'))
    backup_dir = 'farminv-backup-server'
    try:
        backup_list = nc.list(backup_dir)
        if len(backup_list) == 0:
            logging.info('no backup exists create new db on gunicorn start')
        else:
            logging.info(f'fetch last backup in list[{backup_list[-1].path}]')
            backup_dir = '/usr/local/var/app.app-instance'
            os.makedirs(backup_dir)
            nc.get_file(backup_list[-1].path, backup_dir + '/farminv.db')
        logging.info(f'fetch db ok')
    except:
        logging.error('Cant fetch last backup')


def create_backup():
    try:
        if 'NEXTCLOUD_HOST' in os.environ and 'NEXTCLOUD_USER' in os.environ and 'NEXTCLOUD_PASSWORD' in os.environ:
            nc = nextcloud_client.Client(os.environ.get('NEXTCLOUD_HOST'))
            nc.login(os.environ.get('NEXTCLOUD_USER'), os.environ.get('NEXTCLOUD_PASSWORD'))

            backup_dir = 'farminv-backup-server'
            try:
                for element in nc.list(backup_dir):
                    print()
                logging.debug('backup directory on NEXTCLOUD exists')
            except:
                logging.warning('backup directory on NEXTCLOUD does not exist creating...')
                nc.mkdir(backup_dir)
            for dir_path, dir_names, filenames in os.walk("/"):
                for filename in [f for f in filenames if f.endswith("inv.db")]:
                    # normal path : /usr/local/var/app.app-instance/farminv.db
                    backup_name = f'{backup_dir}/{datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}_backup.db'
                    nc.put_file(backup_name, os.path.join(dir_path, filename))

        else:
            raise Exception('Environment variables for backup on nextcloud not set')
    except:
        raise Exception('An error occured during backup creation')
