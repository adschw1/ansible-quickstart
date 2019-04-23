SECONDS=0
ansible-playbook ~/playground/ansithon/prompts.yml -i ~/playground/ansithon/poc_inventory.yaml
sleep 1
ansible-playbook ~/playground/ansithon/prompts.yml -i ~/playground/ansithon/poc_inventory.yaml
sleep 1
ansible-playbook ~/playground/ansithon/poc_playbook.yml -i ~/playground/ansithon/poc_inventory.yaml
sleep 1
ansible-playbook ~/playground/ansithon/poc_playbook.yml -i ~/playground/ansithon/poc_inventory.yaml
echo $SECONDS
