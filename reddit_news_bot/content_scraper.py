from typing import Tuple
import requests
from bs4 import BeautifulSoup, Tag

def get_latest_post(root_url, url, first_class_name) -> Tuple[str, str, str]:
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Response code not successful: { response }')
        raise

    soup = BeautifulSoup(response.content, 'html.parser')

    message_group = soup.find('div', class_=first_class_name)

    if not message_group:
        print('Message group not found')
        raise

    if not isinstance(message_group, Tag):
        print('Message group not expected type')
        raise

    messages = message_group.find_all('div')
    if not messages:
        print('Failed to find any divs')
        raise

    first_message = messages[0]
    main_cell = first_message.find('div', class_='structItem-cell structItem-cell--main')
    if not main_cell:
        print('Failed to find main cell')
        raise

    title = main_cell.find('div', class_='structItem-title')
    if not title:
        print('Failed to find title')
        raise

    link = title.find('a', href=True)
    if not link:
        print('Failed to find linked post')
        raise

    href = link['href']
    new_page_link = root_url + href
    linked_page_response = requests.get(new_page_link)
    if linked_page_response.status_code != 200:
        print('Failed to navigate to linked post')
        raise

    linked_page_soup = BeautifulSoup(linked_page_response.content, 'html.parser')
    title = linked_page_soup.find('h1', class_='p-title-value')
    if not title:
        print('Failed to get title of post')
        raise

    messages = linked_page_soup.find_all('article')
    if not messages:
        print('Failed to find any messages in linked post')
        raise

    first_msg = messages[0]

    if not first_msg:
        print('Failed to get first message in linked post')
        raise

    first_msg_content = first_msg.find('div', class_='bbWrapper')
    return title.get_text(strip=True), first_msg_content, new_page_link
