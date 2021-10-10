import os

import pytest

from http_monitoring.alerting import Alerting
from http_monitoring.time_interval_analyzer import TimeIntervalAnalyzer
from http_monitoring.traffic_analyzer import TrafficAnalyzer
from tests.data import (
    TEST_TRAFFIC_TH,
    TEST_TRAFFIC_INTERVAL,
    TEST_DELAY_IN_STATS,
    TEST_INTERVAL_IN_STATS,
)


@pytest.fixture()
def traffic_analyzer() -> TrafficAnalyzer:
    return TrafficAnalyzer(
        traffic_th=TEST_TRAFFIC_TH, traffic_interval=TEST_TRAFFIC_INTERVAL
    )


@pytest.fixture()
def alerting(traffic_analyzer: TrafficAnalyzer) -> Alerting:
    return Alerting(traffic_analyzer)


@pytest.fixture()
def time_interval_analyzer() -> TimeIntervalAnalyzer:
    return TimeIntervalAnalyzer(
        interval=TEST_INTERVAL_IN_STATS, delay=TEST_DELAY_IN_STATS
    )


@pytest.fixture
def rootdir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def sample_data_csv(rootdir: str):
    return os.path.join(rootdir, "sample_data.csv")
