import os

# path_of_sql= r'/home/amnex/Documents/NMDC_NEW/TEMPLATES/DATABASE/DB_05_JUNE_KIRANDUL_DEFAULT.sql'
path_of_sql= r'D:/code/invoice/database/DB_BACKUP.sql'

# path_of_log= r'/home/amnex/Documents/NMDC_NEW/TEMPLATES/DATABASE/DB_05_JUNE_KIRANDUL_DEFAULT.log'
path_of_log= r'D:/code/invoice/database/DB_BACKUP.log'
###db name
database_name="invoice"
command = r"pg_dump -h localhost -U postgres -p 5432 --verbose {} > {}".format(database_name,path_of_sql)
# print(command)
os.system(command)