Backend of my personal website: http://jasonyue.ca

[Development]
[Virtualenv]
Share venv configurations by freezing and using requirements.txt (while being in the virtualenv)
pip freeze > requirements.txt
--------------------------
[Unix]
source venv/bin/activate
[Windows]
venv\Scripts\activate.bat
--------------------------
pip install -r requirements.txt

[Production]

[To check if ready to deploy]
python manage.py check --deploy --settings=jasonyue.production_settings

[Run before deployment]
python manage.py collectstatic --settings=jasonyue.production_settings

[Run to start production server]
python manage.py runserver --settings=jasonyue.production_settings

[Deployment]

[Upload files to the server]
sudo systemctl restart uwsgi