import datetime
import logging
import os

def configureLogger():
    
    if not os.path.exists('logs'):
        os.makedirs('logs')

    now = datetime.datetime.now()

    loggerOutputFileName = 'logs/' + now.strftime("%d-%m-%Y_%H:%M:%S:%f")
    loggerOutputFileName = loggerOutputFileName + '.log'

    loggerFormat = '%(asctime)s %(levelname)s %(module)s.%(funcName)s'
    loggerFormat += ' [line = %(lineno)d] : %(message)s' 

    logging.basicConfig(format = loggerFormat,
        datefmt = '%m/%d/%Y %I:%M:%S %p',
        filename = loggerOutputFileName,
        level = logging.DEBUG)
        
