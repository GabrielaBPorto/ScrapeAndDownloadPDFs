import utils
import re
from time import sleep

def process_option(option, item, session):
    option_url = utils.ANALYSIS_URL['url'].format(optionValue=option)
    response = session.get(option_url, headers=utils.ANALYSIS_URL['headers'])
    is_file_created = False
    
    links = utils.obtain_links_from_item(response.text)
    for link in links:
        response = utils.handle_http_response(session,url=link)
        if utils.response_is_valid_and_pdf(response):
            utils.create_file(utils.generate_file_name(item), response.content)
            is_file_created = True
            break
        sleep(10)

    return is_file_created

def process_consumer(item, session):
    item_url = utils.CONSUMER_URL['url'].format(consumerValue=item)
    response = session.get(item_url, headers=utils.CONSUMER_URL['headers'])
    data = response.text 
    variable_line = re.search(f"var ${utils.VARIABLE_NAME} = '(.*)'", data)
    if variable_line:
        list = variable_line.group(1)
        values = list.split(',')
        values = [value for value in values if value != '']
    else:
        if utils.DEBUG:
            print("variable was not found in the data")
        return []
    return values

def process(items):
    for index, item in enumerate(items):
        is_file_created = False
        session = utils.create_http_session()
        options = process_consumer(item, session)
        for option in options:
            if is_file_created:
                break
            if len(option) == 0:
                continue
            
            is_file_created = process_option(option, item, session)
            
        total += 1
        if utils.DEBUG:
            print(f'Items processed: {index + 1} of {len(items)}')
        sleep(1)
        session.close()

    print('Finished processing Items.')

def main():
    items = utils.parse_input()
    process(items)
    if utils.DEBUG:
        utils.print_input(items)
        utils.check_items(items)


if __name__ == "__main__":
    main()
