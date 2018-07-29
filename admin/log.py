#!/usr/local/python3
# -*- coding: UTF-8 -*-

import logging,os
from logging.handlers import RotatingFileHandler

LOGDIR = '/var/log/store'
LOGINFO = os.path.join(LOGDIR, 'info.log')
LOGFMT = '%(asctime)s - [%(levelname)s] - %(levelno)s - %(process)d - %(message)s'


log = logging.getLogger(__name__)
log.setLevel(level = logging.INFO)

handler = RotatingFileHandler(LOGINFO,maxBytes = 10240*1024,backupCount = 5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(LOGFMT)
handler.setFormatter(formatter)
    
console = logging.StreamHandler()
console.setLevel(logging.INFO)

log.addHandler(handler)
log.addHandler(console)

if __name__ == '__main__':
    log.info('log start')

