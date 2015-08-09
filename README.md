# NOVA

## Deploying

### List tags:

`ansible-playbook ansible/site.yaml --list-tags`

### List "deploy" tasks:

`ansible-playbook ansible/site.yaml --tags deploy --list-tasks`

### Deploy to staging server(s):

`ansible-playbook -i ansible/inventories/staging ansible/site.yaml --ask-become-pass --tags deploy`

## Roadmap

- mobile-first (Pure.css?)
- i18n
- Fb/Goog auth
- e-mailing
- texting
- background checks
- other (work-permit?) documentation
