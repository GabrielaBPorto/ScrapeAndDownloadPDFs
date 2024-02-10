# ScrapeAndDownloadPDFs

This project consists of two main Python scripts: `script.py` and `utils.py`.

## script.py

`script.py` is the main script of the project. It contains the following functions:

- `process_option(option, item, session)`: This function processes an option by making a GET request to a URL, obtaining links from the response, and creating a file if the response is a valid PDF.

- `process_consumer(item, session)`: This function processes a consumer item by making a GET request to a URL, extracting a variable from the response, and returning a list of values.

- `process(items)`: This function processes a list of items by creating a HTTP session, processing each consumer item, and processing each option.

- `main()`: This is the main function that parses input, processes the items, and checks the items if in debug mode.

## utils.py

`utils.py` is a utility script that contains several helper functions:

- `remove_special_characters(text)`: This function removes special characters from a text string.

- `generate_file_name(item)`: This function generates a file name from an item.

- `check_items(items)`: This function checks if each item has a PDF file.

- `print_input(item)`: This function prints the input item.

- `parse_input(input=sys.stdin.read())`: This function parses the input from the standard input.

- `create_http_session()`: This function creates a HTTP session with retries.

- `handle_http_response(session, url)`: This function handles a HTTP response and returns the response if successful.

- `find_all_links(text)`: This function finds all links in a text string.

- `obtain_links_from_item(text)`: This function obtains links from an item.

- `response_is_valid_and_pdf(response)`: This function checks if a response is valid and is a PDF.

- `create_file(name, content)`: This function creates a file with a given name and content.

## How to Run

To run this project, you can use the following command:

```sh
python script.py
```

Please note that you need to set up your environment variables in a .env file before running the script.

License
This project is licensed under the Creative Commons License - see the LICENSE.md file for details.

Developer
This project was developed by Gabriela Porto.