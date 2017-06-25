import os
import logging

logger = logging.getLogger('LW')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(os.path.expanduser('~/.lw/lw.log'), mode='w')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)