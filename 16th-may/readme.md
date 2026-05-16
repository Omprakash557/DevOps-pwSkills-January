ansible installing on controller Node:

>> sudo apt update
>> sudo apt install software-properties-common
>> sudo add-apt-repository --yes --update ppa:ansible/ansible
>> sudo apt install ansible
>> ansible --version


===== folder structure - domain driven =====

>> mkdir ansible-scripts
>> cd ansible-scripts
>> mkdir ec2
>> cd ec2
>> nano inventory.ini


>> nano <same key PairName>.pem

>> /home/ubuntu/ansible-scripts/ec2/<same key PairName>.pem

======== ping webservers host =======

>> ansible -i inventory.ini webservers -m ping

[webservers]
54.226.99.188 ansible_user=ubuntu ansible_ssh_private_key_file=/home/ubuntu/ansible-scripts/ec2/ansible-key-16thmay.pem

[webservers]
98.81.204.124 ansible_user=ubuntu ansible_ssh_private_key_file=/home/ubuntu/ansible-scripts/ec2/ansible-key-16thmay.pem

======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======	======

Variable: run time - inject (using -e switch) : -e -> extra vars
>> nano variables-demo.yaml

paste the content:

---
- name: CLI Variable Example
  hosts: all

  tasks:

    - name: Print username
      shell: echo "Username is {{ username }}"


>> ansible-playbook -i inv.ini variable-demo.yaml -e "username=Sid"

======	======	======	======	======	======	======	HARD CODED VARIABLES ======	======	======	======	======	======	======	======	======

>> nano variable-demo2.yaml

paste content:

---
- name: Variables Example
  hosts: all

  vars:
    message: "Hello from Ansible Variables"

  tasks:

    - name: Print variable message
      shell: echo "{{ message }}"
      
>> 



















