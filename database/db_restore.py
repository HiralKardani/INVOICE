import os
import time

# path_of_sql = r'/home/amnex/Documents/NMDC_NEW/TEMPLATES/DATABASE/DB_09_NOV_DEFAULT.sql'
path_of_sql = r'D:/code/invoice/database/DB_BACKUP.sql'

database_name = "invoice"
delete_database = 'psql -h localhost -U postgres -p 5432 -c "DROP DATABASE IF EXISTS {};"'.format(database_name)
create_database = 'psql -h localhost -U postgres -p 5432 -c "CREATE DATABASE {};"'.format(database_name)
passowrd_set =  'psql -h localhost -U postgres -p 5432 -c "ALTER USER postgres WITH PASSWORD \'postgres\';"'

restore_command = r"psql -h localhost -U postgres -p 5432 -d {} -1 -f {}".format(database_name,path_of_sql)
os.system(delete_database)
os.system(create_database)
os.system(passowrd_set)
os.system(restore_command)


 

