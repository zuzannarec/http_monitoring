import logging
import sys

handler = logging.StreamHandler(sys.stdout)
log = logging.getLogger("http_monitoring")
log.setLevel(logging.DEBUG)
log.addHandler(handler)
