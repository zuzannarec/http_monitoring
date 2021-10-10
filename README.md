# HTTP Access Log Analyzer with Alerting #
HTTP Access Log Analyzer with Alerting is a console program written in Python.
Requirements:
 - Python3.9
 - optionally Docker (20.10.7)

# Overview #
The project contains two main functionalities: total traffic analysis with alerting and statistics.

Total traffic analyzer takes incoming traffic data as an input and calculates the average total traffic for each past fixed-size period of time (configurable by user).
It uses a sliding window defined as [current_time - window size, current time) time interval.
Whenever the threshold (configurable by user) is exceeded and we are currently not in an alarm state, an alarm event is logged and system is set into alarm state.
When the average total traffic drops again below the threshold a recovery event is logged.
The implementation assumes that the input data is not always in order in terms of timestamp. In total traffic analysis the delayed data is skipped.

Statistics are calculated for every fixed-size and non-overlapping period of time. Default window size is set to 10s and user can adjust this value.
Since statistics are calculated in potentially short non-overlapping windows and data might be out of order, the solution is maintaining two last windows instead of one.
This way delayed records may still be added to correct window if delay is short enough.
As a result more precise statistics are calculated but this introduces a delay in logging statistics from given window.
The delay is configurable and records delayed more than this value are skipped. Default delay is calculated as 0.2 * analyzed time interval [s].
The following statistics are logged:
 - sections with the highest hits
 - number of hits per section per status code

## Install ##
```buildoutcfg
cd http_monitoring

pip install .
```
# Usage #
All available parameters with descriptions are available in help:
```buildoutcfg
http_monitoring --help
```
Run:
```buildoutcfg
http_monitoring --file-path <PATH_TO_INPUT_FILE>

http_monitoring < <PATH_TO_INPUT_FILE>
```

Example:
```buildoutcfg
http_monitoring < <ROOT_DIR>/http_monitoring/tests/sample_data.csv

http_monitoring --file-path <ROOT_DIR>/http_monitoring/tests/sample_data.csv
```

## Use with Dockerfile ##
```buildoutcfg
cd http_monitoring

docker build --tag monitoring .

docker run -i monitoring:latest < <PATH_TO_INPUT_FILE>
```

Example:
```
docker run -i monitoring:latest < "<ROOT_DIR>/http_monitoring/tests/sample_csv.txt"
```

# Tests #
Run:
```buildoutcfg
cd http_monitoring

pip install -r tests/requirements.txt

pytest tests
```

# Code format #
The codebase is formatted according to flake8 and black formatting rules.

Usage:
```buildoutcfg
cd http_monitoring

pip install -r requirements-lint.txt

flake8 .

black .
```

# TODO #
- Replace counter dict in TrafficAnalyzer with ring buffer implemented in fixed size list.
After such change requests_count_per_timestamp object will be allocated only once and all updates will be made within this allocated memory.
It might improve the performance of the analysis.
- The current implementation of TrafficAnalyzer ignores delayed messages (the highest, so far observed timestamp is considered the current time).
To improve the precision of the analysis the delayed messages should be analyzed.
- TimeIntervalAnalyzer could be implemented as ContextManager to ensure that statistics for the last,
 unfinished time interval are logged at exit.
- The input data should be validated to filter out incorrect records.
- The statistics could be extended eg. partition statistics by authuser.
