import csv
from unittest import mock

from http_monitoring.constants import TIMESTAMP_KEY
from http_monitoring.time_interval_analyzer import TimeIntervalAnalyzer
from tests.data import TEST_INTERVAL_IN_STATS


@mock.patch(
    "http_monitoring.time_interval_analyzer.TimeIntervalAnalyzer.print_stats"
)
def test_interval_analyzer_interval_count(
    print_stats_mock, sample_data_csv: str, time_interval_analyzer: TimeIntervalAnalyzer
):
    with open(sample_data_csv) as f:
        reader = csv.DictReader(f)
        min_time = None
        max_time = 0
        for line in reader:
            if min_time is None:
                min_time = int(line[TIMESTAMP_KEY])
            min_time = min(min_time, int(line[TIMESTAMP_KEY]))
            max_time = max(max_time, int(line[TIMESTAMP_KEY]))
            time_interval_analyzer.analyze_request_time(line)
        print_stats_mock(time_interval_analyzer.get_stats())
        expected_intervals_count = int((max_time - min_time) / TEST_INTERVAL_IN_STATS)
        assert expected_intervals_count == print_stats_mock.call_count
