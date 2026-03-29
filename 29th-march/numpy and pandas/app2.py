import logging

'''
logging configuration

log.i -> information
log.d -> debug
log.e -> error
log.w -> warning
'''

# logging -> event -> timeStamp(dd/mm/yyyy :HH:MM:SS:ms) -> track
# asctime
# log file -> app.log

logging.basicConfig(filename='app.log',
                     level=logging.INFO, 
                     format='%(asctime)s - %(levelname)s - '
                     '%(message)s')

logging.info('This is an info message')
logging.debug('This is a debug message')
logging.error('This is an error message')
logging.warning('This is a warning message')

# more log levels

logging.critical('This is a critical message')
