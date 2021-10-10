from http_monitoring.constants import TIMESTAMP_KEY
from http_monitoring.logger import log
from http_monitoring.traffic_analyzer import TrafficAnalyzer


class Alerting:
    def __init__(self, traffic_analyzer: TrafficAnalyzer):
        self.traffic_analyzer = traffic_analyzer
        self.traffic_alert = False

    def check_traffic_alert(self, input_data: dict):
        self.traffic_analyzer.analyze_traffic(int(input_data[TIMESTAMP_KEY]))
        ret, avg = self.traffic_analyzer.verify_threshold_exceeded()
        if ret and not self.traffic_alert:
            log.info(
                f"ALERT: High traffic generated an alert - hits = {avg}, triggered at {self.traffic_analyzer.get_current_time()}"
            )
            self.traffic_alert = True
        elif not ret and self.traffic_alert:
            log.info(
                f"ALERT: Traffic below threshold - hits = {avg}, recovered at {self.traffic_analyzer.get_current_time()}"
            )
            self.traffic_alert = False
