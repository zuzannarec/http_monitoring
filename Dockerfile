FROM docker.io/library/python:3.9-alpine as base

#package
FROM base AS package
COPY . .
RUN python setup.py bdist_wheel --dist-dir=/tmp/dist

# unit tests
FROM package AS unit_tests
RUN pip install pytest
RUN pip install -r tests/requirements.txt
RUN pytest tests || true

#release
FROM base AS release
COPY --from=package /tmp/dist /tmp/dist
RUN pip install /tmp/dist/*.whl

ENTRYPOINT ["python", "-m", "http_monitoring"]

