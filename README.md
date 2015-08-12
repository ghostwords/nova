# nova.jobs

## Deploying

### List tags:

`ansible-playbook ansible/site.yaml --list-tags`

### List "deploy" tasks:

`ansible-playbook ansible/site.yaml --tags deploy --list-tasks`

### Deploy to staging server(s):

`ansible-playbook -i ansible/inventories/staging ansible/site.yaml --ask-become-pass --tags deploy`

## License

The source code is licensed under Mozilla Public License Version 2.0.

All assets (images/logos/branding) are property of Team Nova.
