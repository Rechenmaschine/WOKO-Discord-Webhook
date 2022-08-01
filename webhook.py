import time

from discord_webhook import DiscordEmbed, DiscordWebhook
from configparser import ConfigParser
from room import Room

config = ConfigParser()


def update_config():
    config.read_file(open(r'config.cfg'))


def notify_added(rooms: [Room], content="@everyone new flat available!"):
    update_config()
    for room in rooms:
        for url in config['webhook_urls'].values():
            webhook = DiscordWebhook(url, content=content)
            embed = create_embed(room)
            webhook.add_embed(embed)
            response = webhook.execute()
        time.sleep(0.1)


def notify_removed(rooms: [Room], content="@everyone old flat was taken down!"):
    update_config()
    for room in rooms:
        for url in config['webhook_urls'].values():
            webhook = DiscordWebhook(url, content=content)
            embed = create_embed(room)
            embed.title = "❌ ~~" + embed.title + "~~"
            embed.description = "~~" + embed.description + "~~"
            embed.set_color(0)
            embed.set_footer()
            embed.set_thumbnail()
            webhook.add_embed(embed)
            response = webhook.execute()
        time.sleep(0.1)


def notify_back_online(old_rooms: [Room], new_rooms: [Room]):
    config.read_file(open(r'config.cfg'))

    added_rooms = new_rooms.difference(old_rooms)
    removed_rooms = old_rooms.difference(new_rooms)

    for url in config['webhook_urls'].values():
        message = f"Good morning! During downtime `{len(added_rooms)}` rooms became available. " \
                  f"`{len(removed_rooms)}` rooms were taken down."
        webhook = DiscordWebhook(url, content=message)
        response = webhook.execute()


def create_embed(room):
    embed = DiscordEmbed()
    embed.set_color("ea4c6c")
    embed.set_url(room.url())
    embed.set_title(room.title)
    embed.set_description(room.description)

    embed.add_embed_field(name="Address", value=room.address, inline=True)
    embed.add_embed_field(name="Rent", value=room.price_fmt(), inline=True)
    embed.set_footer(text="Uploaded at " + str(room.submitted))

    embed.set_thumbnail(url="https://www.woko.ch/images/logos/woko-logo.png")

    return embed
