import os
import pathlib
import requests


# Get the rquest url from the response
def get_request_url(provided_url: str) -> str:
    return requests.get(url=provided_url).url

# Get the file extension
def get_file_extension(system_path: str) -> str:
    return pathlib.Path(system_path).suffix


# Check if a file exists
def check_file_exists(system_path: str) -> bool:
    return os.path.isfile(path=system_path)


def main() -> None:
    # Get the headers from the response
    print(get_request_url(provided_url="https://www.example.com"))


main()