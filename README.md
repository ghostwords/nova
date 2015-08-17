# nova.jobs

Django project in `django/`, Ansible provisioning and deployment stuff in `ansible/`. Switch to `django/` before working on the site. Don't switch to `ansible/` when provisioning/deploying though ...


## Development set up

1. Install dependencies from `django/requirements-dev.txt`. You probably want to use `pip` and `virtualenv`. Note this is a Python 3 project.
2. TODO Database/admin user setup.


## Working on the site

Run `python manage.py runserver` from the `django/` project directory.


## Working with translations

Whenever translations need to be updated:

1. Run `dj makemessages` (assuming bash alias from above) to regenerate locale files.
2. Start the dev server, log in as the admin user to admin UI.
3. Go to `localhost/rosetta` and start updating translations. Much better than editing po files by hand. No need to run `dj compilemessages` since Rosetta does that for you when you save.


## Deploying

List tags:

`ansible-playbook ansible/site.yaml --list-tags`

List "deploy" tasks:

`ansible-playbook ansible/site.yaml --tags deploy --list-tasks`

Deploy to staging server(s):

`ansible-playbook ansible/site.yaml -i ansible/staging --ask-vault-pass --ask-become-pass --tags deploy`

Actually ... The same server is currently used for staging and production domains, but we vary the domain variable in the inventory.


## License

The source code is licensed under Mozilla Public License Version 2.0.

All assets (images/logos/branding) are property of Team Nova.
