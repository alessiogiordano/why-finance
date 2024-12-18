#
#  crawler.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

import time
from services.crawler_service import CrawlerService

from utils.logger import logger
#-----------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    crawler = CrawlerService()
    count = 0
    while True:
        try:
            crawler.collect_data()
            logger.info(f"Ciclo di inserimento n. {count} completato.")
            count += 1
            time.sleep(crawler.crawler_time_interval)
        except Exception as e:
            logger.error(f"Errore durante il ciclo principale: {e}")
            break