import json
from typing import Callable, Any

from http_monitoring.constants import (
    REQUEST_KEY,
    MAX_KEY_STATS_KEY,
    STATUS_KEY,
    STATUS_CODES_SUMMARY_KEY,
)
from http_monitoring.logger import log
from http_monitoring.section import Section


class Stats:
    def __init__(self, log_func: Callable, msg: str, value: Any):
        self.log_func = log_func
        self.msg = msg
        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=4)
        self.value = value

    def log_stats(self):
        self.log_func(f"STATS: {self.msg} {self.value}")


class StatisticsAnalyzer:
    def __init__(self):
        self.stats = dict()
        self.sections = dict()
        self.status_codes = dict()

    def update_stats(self, input_data: dict) -> None:
        http_method, url, _ = input_data[REQUEST_KEY].split(" ")
        status_code = input_data[STATUS_KEY]
        section_name = "/" + url.split("/")[1]

        # update data required to prepare list of sections with the most hits
        if section_name not in self.sections.keys():
            self.sections[section_name] = Section(section_name)
        self.sections[section_name].increase_hits_count(1)

        # update data required to prepare summary of returned status codes
        if status_code not in self.status_codes.keys():
            self.status_codes[status_code] = dict()
        if section_name not in self.status_codes[status_code].keys():
            self.status_codes[status_code][section_name] = 0
        self.status_codes[status_code][section_name] += 1

    def get_stats(self) -> dict:
        hits_count = self.get_most_hit_sections()
        if hits_count:
            self.stats[MAX_KEY_STATS_KEY] = Stats(
                log.info, "Highest hits in the last 10 s:", hits_count
            )
        status_code_summary = self.get_status_codes_summary()
        if status_code_summary:
            self.stats[STATUS_CODES_SUMMARY_KEY] = Stats(
                log.debug, "Status codes summary in the last 10s:", status_code_summary
            )
        return self.stats

    def cleanup(self) -> None:
        self.stats = dict()
        self.sections = dict()
        self.status_codes = dict()

    def get_most_hit_sections(self, count: int = 5) -> (str, None):
        hits_count = list()
        for section_name, section in self.sections.items():
            hits_count.append((section_name, section.get_hits_count()))
        hits_count.sort(key=lambda x: x[-1])
        if hits_count:
            return hits_count[:count]
        return None

    def get_status_codes_summary(self) -> (str, None):
        if self.status_codes:
            return self.status_codes
        return None
