import sys
import json

from lf_toolkit.evaluation import Params
from .evaluation import evaluation_function
from .preview import preview_function

def handle_request(req):
    command = req.get('command', None)

    if command == 'eval':
        response = req.get('response', None)
        answer = req.get('answer', None)
        params = Params(req.get('params', {}))
        return command, evaluation_function(response, answer, params)
    elif command == 'preview':
        response = req.get('response', None)
        params = Params(req.get('params', {}))
        return command, preview_function(response, params)
    else:
        raise ValueError(f'Unknown command: {command}')

def main():
    try:
        if len(sys.argv) != 3:
            raise ValueError('Usage: python -m evaluation_function.main <request_file_path> <response_file_path>')

        # Read the request file path and response file path from command-line arguments
        request_file_path = sys.argv[1]
        response_file_path = sys.argv[2]

        # Read the request data from the request file
        with open(request_file_path, 'r') as request_file:
            request_data = json.load(request_file)

        # Handle the request
        command, result =handle_request(request_data)

        # Prepare the response data
        response = {"command": command, "result": result}

        # Write the response data to the response file
        with open(response_file_path, 'w') as response_file:
            json.dump(response, response_file)

    except Exception as e:
        # Write any error messages to stderr
        sys.stderr.write(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()