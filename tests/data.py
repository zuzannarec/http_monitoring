TEST_TRAFFIC_TH = 1
TEST_TRAFFIC_INTERVAL = 5

TEST_INTERVAL_IN_STATS = 10
TEST_DELAY_IN_STATS = 2


def input_data() -> list:
    return [
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573860",
            "request": "GET /api/user HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.4",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573861",
            "request": "GET /api/user HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.4",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573860",
            "request": "GET /api/user HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573862",
            "request": "GET /api/help HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.5",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573863",
            "request": "GET /api/help HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.4",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573864",
            "request": "GET /api/help HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.5",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573866",
            "request": "POST /report HTTP/1.0",
            "status": "500",
            "bytes": "1307",
        },
        {
            "remotehost": "10.0.0.3",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573866",
            "request": "POST /report HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.3",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573865",
            "request": "GET /report HTTP/1.0",
            "status": "200",
            "bytes": "1194",
        },
        {
            "remotehost": "10.0.0.4",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573866",
            "request": "GET /api/user HTTP/1.0",
            "status": "200",
            "bytes": "1136",
        },
        {
            "remotehost": "10.0.0.1",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573867",
            "request": "GET /api/user HTTP/1.0",
            "status": "200",
            "bytes": "1261",
        },
        {
            "remotehost": "10.0.0.3",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573869",
            "request": "GET /api/help HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573869",
            "request": "GET /api/help HTTP/1.0",
            "status": "200",
            "bytes": "1194",
        },
        {
            "remotehost": "10.0.0.5",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573873",
            "request": "GET /api/help HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573873",
            "request": "GET /report HTTP/1.0",
            "status": "200",
            "bytes": "1136",
        },
    ]


def expected_traffic_average_values() -> list:
    return [
        (False, 0.2),
        (False, 0.4),
        (False, 0.6),
        (False, 0.8),
        (True, 1.0),
        (True, 1.2),
        (False, 0.8),
        (True, 1.0),
        (True, 1.2),
        (True, 1.4),
        (True, 1.4),
        (True, 1.2),
        (True, 1.4),
        (False, 0.6),
        (False, 0.8),
    ]


def input_data_delay() -> list:
    return [
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573860",
            "request": "GET /api/user HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.4",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573861",
            "request": "GET /api/user HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.4",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573859",
            "request": "GET /api/user HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573862",
            "request": "GET /api/help HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
        {
            "remotehost": "10.0.0.5",
            "rfc931": "-",
            "authuser": "apache",
            "date": "1549573863",
            "request": "GET /api/help HTTP/1.0",
            "status": "200",
            "bytes": "1234",
        },
    ]


EXPECTED_ALERTS = [
    "ALERT: High traffic generated an alert - hits = 1.0, triggered at 1549573863",
    "ALERT: Traffic below threshold - hits = 0.8, recovered at 1549573866",
    "ALERT: High traffic generated an alert - hits = 1.0, triggered at 1549573866",
    "ALERT: Traffic below threshold - hits = 0.6, recovered at 1549573873",
]
