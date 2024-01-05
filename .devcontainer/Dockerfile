# Build Base Image
ARG PYTHON_VARIANT=3.10.7
FROM --platform=linux/amd64 python:${PYTHON_VARIANT} as ap_playground_base
# Install Requirements
COPY ./requirements.txt /usr/local/
RUN pip install --retries 5 -r /usr/local/requirements.txt