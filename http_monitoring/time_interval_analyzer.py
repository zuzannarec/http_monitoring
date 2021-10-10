from http_monitoring.constants import TIMESTAMP_KEY
from http_monitoring.logger import log
from http_monitoring.statistics_analyzer import StatisticsAnalyzer


class TimeIntervalAnalyzer:
    def __init__(self, interval: int, delay: int):
        # required to analyze delayed messages
        self.stats_analyzer_prior = StatisticsAnalyzer()
        self.stats_analyzer_current = StatisticsAnalyzer()
        self.interval_start_time = None
        self.current_time = 0
        self.interval = interval
        self.delay = delay
        self.initial_interval = True

    def analyze_request_time(self, line: dict) -> None:
        request_time = int(line[TIMESTAMP_KEY])
        self.current_time = max(self.current_time, request_time)

        self._update_interval_start(request_time)

        if request_time >= self.interval_start_time:
            self.stats_analyzer_current.update_stats(line)
        elif self._check_if_message_in_delay_range(request_time):
            self.stats_analyzer_prior.update_stats(line)
        else:
            log.warning(f"Skipping delayed message with request time: {request_time}")

        self._log_stats()

    def get_stats(self) -> dict:
        return self.stats_analyzer_prior.get_stats()

    def flush(self) -> dict:
        stats = self.stats_analyzer_prior.get_stats()
        if stats:
            return stats
        return self.stats_analyzer_current.get_stats()

    def _update_stats_analyzer(self, request_time: int, line: dict) -> None:
        if request_time >= self.interval_start_time:
            self.stats_analyzer_current.update_stats(line)
        elif self._check_if_message_in_delay_range(request_time):
            self.stats_analyzer_prior.update_stats(line)
        else:
            log.warning(f"Skipping delayed message with request time: {request_time}")

    def _update_interval_start(self, request_time: int) -> None:
        if self.interval_start_time is None:
            self.interval_start_time = request_time
        elif request_time >= self.interval_start_time + self.interval:
            # start new stats interval
            self.interval_start_time = self.interval_start_time + self.interval
            self.stats_analyzer_prior = self.stats_analyzer_current
            self.stats_analyzer_current = StatisticsAnalyzer()

    def _log_stats(self) -> None:
        # the allowed delay exceeded, log statistics from the last complete interval
        stats = self.get_stats()
        if self.current_time >= self.interval_start_time + self.delay and stats:
            # stats for the delayed messages in the initial interval should be ignored
            # as they do not consider all messages from the pre-analysis interval
            if self.initial_interval:
                self.initial_interval = False
                self.stats_analyzer_prior.cleanup()
                return
            TimeIntervalAnalyzer.print_stats(stats)
            self.stats_analyzer_prior.cleanup()

    def _check_if_delayed_message(self, request_time: int) -> bool:
        return request_time < self.interval_start_time

    def _check_if_message_in_delay_range(self, request_time: int) -> bool:
        # message is delayed, check if it was received within the allowed delay range
        return (
            self._check_if_delayed_message(request_time)
            and self.current_time < self.interval_start_time + self.delay
        )

    @staticmethod
    def print_stats(stats: dict):
        for stats in stats.values():
            stats.log_stats()
