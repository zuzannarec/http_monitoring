from collections import Counter

from http_monitoring.logger import log


class TrafficAnalyzer:
    def __init__(self, traffic_th: int, traffic_interval: int):
        self.traffic_th = traffic_th
        self.traffic_interval = traffic_interval
        self.interval_start_time = None
        # TODO replace requests_count_per_timestamp Counter dict with ring buffer implemented on fixed size list
        self.requests_count_per_timestamp = Counter()
        self.requests_count = 0
        self.current_time = 0

    def analyze_traffic(self, request_time: int) -> None:
        if not isinstance(request_time, (int, float)):
            raise ValueError(f"Invalid request date type: {type(request_time)}")
        if self.interval_start_time is None:
            self.interval_start_time = request_time
        if self._check_if_delayed_message(request_time):
            log.info(f"Delayed message: {request_time}. Skipping...")
            return
        self._forward_time_window(request_time)
        self._update_requests_count_summary(request_time)

    def _check_if_delayed_message(self, request_time: int) -> bool:
        return request_time < self.interval_start_time

    def _forward_time_window(self, request_time: int):
        if request_time < self.interval_start_time + self.traffic_interval:
            return
        # move interval_start_time forward and reduce the total count of requests
        while self.interval_start_time <= request_time - self.traffic_interval:
            self.requests_count -= self.requests_count_per_timestamp.pop(
                self.interval_start_time, 0
            )
            self.interval_start_time += 1

    def _update_requests_count_summary(self, request_time: int) -> None:
        self.current_time = max(self.current_time, request_time)
        # increase the total count of requests
        self.requests_count += 1
        # store number of requests per second
        self.requests_count_per_timestamp[request_time] += 1

    def verify_threshold_exceeded(self) -> (bool, float):
        average_traffic = self.calculate_average()
        return average_traffic >= self.traffic_th, average_traffic

    def calculate_average(self) -> float:
        return self.requests_count / self.traffic_interval

    def get_time_window_range(self) -> (int, int):
        return self.interval_start_time, self.current_time

    def get_current_time(self) -> int:
        return self.current_time
