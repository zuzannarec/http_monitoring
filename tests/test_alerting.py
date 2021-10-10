from unittest import mock

from http_monitoring.alerting import Alerting
from tests.data import input_data, EXPECTED_ALERTS


@mock.patch("http_monitoring.alerting.log")
def test_alerting(log, alerting: Alerting):
    for line in input_data():
        alerting.check_traffic_alert(line)
    for log_msg, alert_msg in zip(log.info.call_args_list, EXPECTED_ALERTS):
        assert log_msg[0][0] == alert_msg
