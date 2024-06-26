# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from communities_modules.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new twitch channel from a given payload. Throws an error if no payload is given, or the twitch channel already exists.
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'channel' not in payload or 'community_id' not in payload or 'servers' not in payload or 'aliases' not in payload:
        return dict(msg="Payload missing required fields.")
    if db((db.twitch.channel == payload['channel']) & (db.twitch.community_id == payload['community_id'])).count() > 0:
        return dict(msg="Twitch channel already exists.")
    db.twitch.insert(**payload)
    return dict(msg="Twitch channel created.")

# Get all twitch channels.
def get_all():
    twitch_channels = db(db.twitch).select()
    return dict(data=twitch_channels)

# Get a twitch channel by its channel name. If the twitch channel does not exist, return an error.
def get_by_channel():
    channel = request.args(0)
    channel = decode_name(channel)
    if not channel:
        return dict(msg="No channel name given.")
    twitch_channel = db(db.twitch.channel == channel).select().first()
    if not twitch_channel:
        return dict(msg="Twitch channel does not exist.")
    return dict(data=twitch_channel)

# Update a twitch channel by its channel name. If the twitch channel does not exist, return an error.
def update_by_channel():
    channel = request.args(0)
    channel = decode_name(channel)
    if not channel:
        return dict(msg="No channel name given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'channel' not in payload or 'community_id' not in payload or 'servers' not in payload or 'aliases' not in payload:
        return dict(msg="Payload missing required fields.")
    twitch_channel = db(db.twitch.channel == channel).select().first()
    if not twitch_channel:
        return dict(msg="Twitch channel does not exist.")
    twitch_channel.update_record(**payload)
    return dict(msg="Twitch channel updated.")

# Delete a twitch channel by its channel name. If the twitch channel does not exist, return an error.
def delete_by_channel():
    channel = request.args(0)
    channel = decode_name(channel)
    if not channel:
        return dict(msg="No channel name given.")
    twitch_channel = db(db.twitch.channel == channel).select().first()
    if not twitch_channel:
        return dict(msg="Twitch channel does not exist.")
    twitch_channel.delete_record()
    return dict(msg="Twitch channel deleted.")