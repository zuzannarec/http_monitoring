import pytest

from http_monitoring.constants import TIMESTAMP_KEY
from http_monitoring.traffic_analyzer import TrafficAnalyzer
from tests.data import (
    input_data,
    expected_traffic_average_values,
    TEST_TRAFFIC_INTERVAL,
    input_data_delay,
)


def test_analyze_traffic_average_value(traffic_analyzer: TrafficAnalyzer):
    for line, result in zip(input_data(), expected_traffic_average_values()):
        traffic_analyzer.analyze_traffic(int(line[TIMESTAMP_KEY]))
        assert traffic_analyzer.verify_threshold_exceeded() == result


def test_analyze_time_window_range(traffic_analyzer: TrafficAnalyzer):
    for idx, line in enumerate(input_data()):
        traffic_analyzer.analyze_traffic(int(line[TIMESTAMP_KEY]))
        if idx >= TEST_TRAFFIC_INTERVAL:
            assert (
                traffic_analyzer.get_time_window_range()[1]
                == traffic_analyzer.get_time_window_range()[0]
                + TEST_TRAFFIC_INTERVAL
                - 1
            )
        else:
            assert (
                traffic_analyzer.get_time_window_range()[1]
                >= traffic_analyzer.get_time_window_range()[0]
            )


def test_skip_time_invalid_format(traffic_analyzer: TrafficAnalyzer):
    with pytest.raises(ValueError) as _:
        traffic_analyzer.analyze_traffic("1549573863")


def test_skip_delayed_input(traffic_analyzer: TrafficAnalyzer):
    for line in input_data_delay():
        traffic_analyzer.analyze_traffic(int(line[TIMESTAMP_KEY]))
    assert traffic_analyzer.requests_count == len(input_data_delay()) - 1
    assert (
        traffic_analyzer.calculate_average()
        == (len(input_data_delay()) - 1) / TEST_TRAFFIC_INTERVAL
    )
