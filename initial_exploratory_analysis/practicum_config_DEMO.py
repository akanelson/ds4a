# Rename this file to practicum_config.py
# IMPORTANT: Once renamed this file should never be uploaded to repository!

postgre_user = '[POSRGRES USER]'
postgre_pass = '[PASSWORD]'
postgre_host = 'localhost'
postgre_db   = '[DB_NAME]'


postgre_conn = 'postgresql://{}:{}@{}/{}'.format(postgre_user, postgre_pass, postgre_host, postgre_db)