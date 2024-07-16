from src.utils import db_conn
import logging

# setting up logging
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

def database_connection():
    logger.info('Connecting to database...')
    try:
        db_conn.DbConn('movieDb')
    except Exception as e:
        logger.error('Failed to connect to database: %s', e)
        return

    logger.info('Connected to database')

def main():
    logger.info('Starting up...')
    database_connection()
    logger.info('Shutting down...')


if __name__ == '__main__':
    main()
