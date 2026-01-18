from locust import LoadTestShape
from config.config import cfg, logger


class CustomLoadShape(LoadTestShape):
    """
        Здесь должны быть описаны типы нагрузки с помощью stages
    """
    
    def __init__(self):  
        super().__init__()
        match cfg.loadshape_type:
            case "baseline":
                self.stages = [
                    {"duration": 5, "users": 1, "spawn_rate": 1}
                ]
            case "stages":
                self.stages = [
                    {"duration": 60, "users": 10, "spawn_rate": 1},
                    {"duration": 120, "users": 20, "spawn_rate": 2},
                    {"duration": 180, "users": 30, "spawn_rate": 1},
                    {"duration": 240, "users": 40, "spawn_rate": 1},
                ]
    
    def tick(self): 
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None