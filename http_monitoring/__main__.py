import argparse
import csv
import os
import sys
from typing import TextIO

from http_monitoring.alerting import Alerting
from http_monitoring.constants import HEADER
from http_monitoring.logger import log
from http_monitoring.time_interval_analyzer import TimeIntervalAnalyzer
from http_monitoring.traffic_analyzer import TrafficAnalyzer

INTERVAL_TIME_S = 10
DELAY_TIME_S = INTERVAL_TIME_S * 0.2
TRAFFIC_TH = 10
TRAFFIC_INTERVAL_S = 120


def _file_exists(file_path):
    if os.path.isfile(file_path):
        return file_path
    raise argparse.ArgumentTypeError(
        "Provided path is invalid or the file does not exist"
    )


parser = argparse.ArgumentParser(
    description="HTTP Log Monitoring - send data to STDIN or provide input file"
)
parser.add_argument(
    "--file-path", type=_file_exists, help="Input file path (CSV format)", default=None
)
parser.add_argument("--delimiter", help="Delimiter in input data", default=",")
parser.add_argument(
    "--no-header",
    action="store_true",
    help="Set if input file does not contain header. Default header will be used.",
)
parser.add_argument(
    "--interval",
    type=int,
    help="Interval [s] in which statistics are calculated",
    default=INTERVAL_TIME_S,
)
parser.add_argument(
    "--delay",
    type=int,
    help="Acceptable delay [s] of log message. \
                          When exceeded in relation to the end of the analyzed interval, the message is skipped.",
    default=DELAY_TIME_S,
)
parser.add_argument(
    "--traffic-th",
    type=int,
    help="Minimum average number of requests per second to trigger traffic alert",
    default=TRAFFIC_TH,
)
parser.add_argument(
    "--traffic-interval",
    type=int,
    help="Interval [s] in which an average traffic is calculated",
    default=TRAFFIC_INTERVAL_S,
)
args = parser.parse_args()


def analyze_data(
    reader: csv.DictReader,
    alerting: Alerting,
    time_interval_analyzer: TimeIntervalAnalyzer,
) -> None:
    for line in reader:
        alerting.check_traffic_alert(line)
        time_interval_analyzer.analyze_request_time(line)
    TimeIntervalAnalyzer.print_stats(time_interval_analyzer.flush())


def create_reader(
    input_data: TextIO, delimiter: str, no_header: bool
) -> csv.DictReader:
    fieldnames = None
    if no_header:
        fieldnames = HEADER
    return csv.DictReader(input_data, fieldnames=fieldnames, delimiter=delimiter)


def main():
    traffic_analyzer = TrafficAnalyzer(args.traffic_th, args.traffic_interval)
    alerting = Alerting(traffic_analyzer)
    time_interval_analyzer = TimeIntervalAnalyzer(args.interval, args.delay)
    try:
        if args.file_path:
            log.info(f"Reading input file {args.file_path}")
            # TODO modify reading input file to wait for new data instead of closing the file after reaching the end
            with open(args.file_path) as f:
                reader = create_reader(f, args.delimiter, args.no_header)
                analyze_data(reader, alerting, time_interval_analyzer)
        else:
            log.info("Data file path not provided. Waiting for input...")
            reader = create_reader(sys.stdin, args.delimiter, args.no_header)
            analyze_data(reader, alerting, time_interval_analyzer)
    except KeyboardInterrupt:
        log.info("\nExiting...")
        sys.exit()


if __name__ == "__main__":
    main()
