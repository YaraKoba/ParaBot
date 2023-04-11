DJANGO_MANAGE=python django_admin/service/manage.py
DJANGO_SETTINGS_MODULE=service.settings

requirements:
	pip install --upgrade pip
	pip install -r requirements.txt

migrate:
	$(DJANGO_MANAGE) makemigrations --settings=$(DJANGO_SETTINGS_MODULE)
	$(DJANGO_MANAGE) migrate --settings=$(DJANGO_SETTINGS_MODULE)

createsuperuser:
	$(DJANGO_MANAGE) createsuperuser --settings=$(DJANGO_SETTINGS_MODULE)

runserver:
	$(DJANGO_MANAGE) runserver --settings=$(DJANGO_SETTINGS_MODULE)

env_bot:
		echo "TOKEN=\nAPI_KEY=\nADMIN_LOGIN=\nADMIN_PASSWORD=" > para_kzn_bot/.env
		vim para_kzn_bot/.env
		vim para_kzn_bot/bot/suport_fl/set_up.py

run_bot:
		python para_kzn_bot/bot/main.py

reminder:
		python para_kzn_bot/bot/reminder.py
