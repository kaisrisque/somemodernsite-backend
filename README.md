**Backend of my personal website: http://jasonyue.ca**

Certain files are "hidden" for security purposes, but there are restrictions already in place so there really is no need.

# Projects

## Blog

Both blog versions are compatible, due to the fact that they expose the same JSON subject. However, v2 has more features and is more robust.

All of the blogs are served through the API.

### Blog v1

This is a simple blog that is built from a tutorial. It can easily be expanded, but would take some time to setup.

### Blog v2

This is the new blog systen that uses a Django package called Wagtail. It is feature-rich and allows for delivering data through an API.

It's compatible with the current v1 system and does not require much modifications on the frontend, since it purposely has the same subjects as v1.

The API link is different though.

## Tic-Tac-Toe

Each request should contain the current board and the player who has moved. 

### AI

The backend for the AI uses a "private" connection, or in other words, it only communicates with the connected client.

### Multiplayer

The backend for multiplayer can technically handle many players, but should only hae 2 players actually playing.

## Chat

The chat backend does not store any of the message, but instead simply broadcasts all received messages asap.

## Websocket

This is a simple app that routes all websocket data to the correct destination.

# Development

## Virtualenv

Share venv configurations by freezing and using requirements.txt (while being in the virtualenv).

pip freeze > requirements.txt.

pip install -r requirements.txt

### Unix

source venv/bin/activate

### Windows

venv\Scripts\activate.bat

# Production

## To check if ready to deploy

python manage.py check --deploy --settings=jasonyue.production_settings

## Run before deployment

python manage.py collectstatic --settings=jasonyue.production_settings

## Run to start production server

python manage.py runserver --settings=jasonyue.production_settings

# Deployment

The server has a script that can be run at any time and will update both the front and backend.

cd /mysite

source ./push.sh