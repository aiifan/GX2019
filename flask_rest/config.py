USERNAME = 'root'
PASSWORD = '123456'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'test'

DIALECT = 'mysql'
DRIVER = 'pymysql'

DB_URL = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)