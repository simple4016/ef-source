import logging


logger = logging.getLogger('cff-finance')
handler = logging.FileHandler('./cff-finance.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
