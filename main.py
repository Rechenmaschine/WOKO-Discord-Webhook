import time
import copy
import requests
import jsonpickle
import webhook
from bs4 import BeautifulSoup
from datetime import datetime
from configparser import ConfigParser
from room import Room


url = "https://www.woko.ch/en/zimmer-in-zuerich"
new_rooms = set()

config = ConfigParser()
config.read_file(open('config.cfg'))


def update_entries():
    print("Updating entries: " + datetime.now().__format__("%H:%M:%S"))
    html = requests.get(url).text
    parsed_html = BeautifulSoup(html, features="html.parser")
    room_elements = parsed_html.find_all('div', attrs={'class': 'inserat'})

    for r in room_elements:
        inserat_id = int(r.a["href"].split('/')[3])
        title_element = r.find('div', attrs={'class': 'titel'})
        title = title_element.h3.text.strip()
        submitted = datetime.strptime(title_element.span.text.strip(), "%d.%m.%Y %H:%M")

        price = int(r.find('div', attrs={'class': 'preis'}).text.rstrip(".-"))
        table = r.table.find_all('td')
        description = table[0].text.strip() + " " + table[1].text.strip()
        address = table[3].text.strip()

        new_rooms.add(Room(inserat_id, title, description, address, submitted, price))


try:
    with open('savestate.json') as json_file:
        old_rooms = jsonpickle.loads(json_file.read())
except FileNotFoundError:
    old_rooms = set()

update_entries()
webhook.notify_back_online(old_rooms, new_rooms)

while True:
    update_entries()
    added_rooms = new_rooms.difference(old_rooms)
    removed_rooms = old_rooms.difference(new_rooms)

    write_json = False

    if len(added_rooms):
        print("New room(s) online!")
        webhook.notify_added(added_rooms)
        write_json = True

    if len(removed_rooms):
        print('Old room(s) offline!')
        webhook.notify_removed(removed_rooms)
        write_json = True

    if write_json:
        with open('savestate.json', 'w') as outfile:
            outfile.write(jsonpickle.dumps(new_rooms))

    time.sleep(float(config['woko-bot']['wait_time']))

    old_rooms = copy.deepcopy(new_rooms)
    new_rooms.clear()
