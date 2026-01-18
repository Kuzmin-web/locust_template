""" Точка входа в тест, 
    описание логики импорта сценариев
"""

from config.config import cfg, logger
from custom_shape.custom_load_shapes import CustomLoadShape

if cfg.webtours_base.included:
    from user_classes.wt_base_scenario import WebToursBaseUserClass
    WebToursBaseUserClass.weight = cfg.webtours_base.weight

    logger.info("WebToursBaseUserClass started")
