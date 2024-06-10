# Base image that bundles AWS Lambda Python 3.9 image with some middleware functions

# TODO: change the base image tag to the latest version
FROM ghcr.io/lambda-feedback/baseevalutionfunctionlayer:pr-10-3.9

# Install git so we can install python packages from git repositories
RUN yum update -y && \
    yum install -y git && \
    yum clean all

# Copy and install any packages/modules needed for your evaluation script.
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip3 install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy helpers
COPY parse.py ${LAMBDA_TASK_ROOT}/app/

# Copy the evaluation and testing scripts
COPY evaluation.py ${LAMBDA_TASK_ROOT}/app/
COPY evaluation_tests.py ${LAMBDA_TASK_ROOT}/app/

# Copy the preview and testing scripts
COPY preview.py ${LAMBDA_TASK_ROOT}/app/
COPY preview_tests.py ${LAMBDA_TASK_ROOT}/app/

# Copy Documentation
COPY docs/dev.md ${LAMBDA_TASK_ROOT}/app/docs/dev.md
COPY docs/user.md ${LAMBDA_TASK_ROOT}/app/docs/user.md

# Set permissions so files and directories can be accessed on AWS
RUN chmod 644 $(find . -type f)
RUN chmod 755 $(find . -type d)

# The entrypoint for AWS is to invoke the handler function within the app package
CMD [ "app.handler.handler" ]
