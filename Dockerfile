FROM ghcr.io/lambda-feedback/evaluation-function-base/python:3.12

# Copy and install any packages/modules needed for your evaluation script.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the evaluation function to the app directory
COPY . .

# Command to start the evaluation function with
ENV FUNCTION_COMMAND="python"

# Args to start the evaluation function with
ENV FUNCTION_ARGS="-m,evaluation_function.main"

# Interface to use for the evaluation function
ENV FUNCTION_INTERFACE="file"