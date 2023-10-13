import nextcloud_client
import os

if __name__ == '__main__':
    nc = nextcloud_client.Client(os.environ.get('NEXTCLOUD_HOST'))
    nc.login(os.environ.get('NEXTCLOUD_USER'), os.environ.get('NEXTCLOUD_PASSWORD'))

    backup_dir = 'farminv-backup-server'
    try:
        backup_list = nc.list(backup_dir)
        if len(backup_list) == 0:
            print('no backup exists create new db on gunicorn start')
        else:
            print(f'fetch last backup in list[{backup_list[-1]}]')
            nc.get_file(backup_list[-1].path, '/usr/local/var/app.app-instance/farminv.db')
    except:
        raise FileNotFoundError
