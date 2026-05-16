# Ansible Setup & Configuration Guide

A comprehensive guide to installing Ansible on a controller node, configuring inventory, and working with playbooks including variables, loops, conditions, and handlers.

---

## 📋 Table of Contents
1. [Installation on Controller Node](#installation-on-controller-node)
2. [Folder Structure](#folder-structure)
3. [Ping WebServers](#ping-webservers)
4. [Runtime Variables (CLI Injection)](#runtime-variables-cli-injection)
5. [Hard-coded Variables](#hard-coded-variables)
6. [Loops](#loops)
7. [Conditions](#conditions)
8. [Handlers](#handlers)

---

## Installation on Controller Node

Update your system and install Ansible:

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
ansible --version
```

---

## Folder Structure

Create a domain-driven folder structure for your Ansible scripts:

```bash
mkdir ansible-scripts
cd ansible-scripts
mkdir ec2
cd ec2
```

This structure keeps your playbooks and inventory files organized:

```
ansible-scripts/
└── ec2/
    ├── inventory.ini
    ├── ansible-key-16thmay.pem (or your key pair name)
    ├── variable-demo.yaml
    ├── variable-demo2.yaml
    ├── loops-example.yaml
    ├── condition-example.yaml
    └── handlers-ex.yaml
```

---

## Ping WebServers

### Create Inventory File

```bash
nano inventory.ini
```

**inventory.ini content:**

```ini
[webservers]
54.226.99.188 ansible_user=ubuntu ansible_ssh_private_key_file=/home/ubuntu/ansible-scripts/ec2/ansible-key-16thmay.pem
98.81.204.124 ansible_user=ubuntu ansible_ssh_private_key_file=/home/ubuntu/ansible-scripts/ec2/ansible-key-16thmay.pem
```

### Add Your SSH Key

Copy your key pair to the ec2 folder:

```bash
nano <same key PairName>.pem
# Copy the private key content here
# Save: Ctrl+X → Y → Enter
```

Set proper permissions:

```bash
chmod 400 "<same key PairName>.pem"
```

### Test Connectivity

Ping all webservers to verify SSH connectivity:

```bash
ansible -i inventory.ini webservers -m ping
```

**Expected Output:**
```
54.226.99.188 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
98.81.204.124 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

---

## Runtime Variables (CLI Injection)

Inject variables at runtime using the `-e` (extra vars) flag.

### Create Playbook

```bash
nano variable-demo.yaml
```

**variable-demo.yaml content:**

```yaml
---
- name: CLI Variable Example
  hosts: all
  tasks:
    - name: Print username
      shell: echo "Username is {{ username }}"
```

### Run with Runtime Variables

```bash
ansible-playbook -i inventory.ini variable-demo.yaml -e "username=Sid"
```

### Multiple Runtime Variables

```bash
ansible-playbook -i inventory.ini variable-demo.yaml -e "username=Sid department=Engineering"
```

---

## Hard-coded Variables

Define variables directly in the playbook.

### Create Playbook

```bash
nano variable-demo2.yaml
```

**variable-demo2.yaml content:**

```yaml
---
- name: Variables Example
  hosts: all
  vars:
    message: "Hello from Ansible Variables"
    app_name: "MyApplication"
    environment: "production"
  tasks:
    - name: Print variable message
      shell: echo "{{ message }}"
    
    - name: Print app name and environment
      shell: echo "App: {{ app_name }}, Env: {{ environment }}"
```

### Run Playbook

```bash
ansible-playbook -i inventory.ini variable-demo2.yaml
```

---

## Loops

Iterate over a list of items in your playbook.

### Create Playbook

```bash
nano loops-example.yaml
```

**loops-example.yaml content:**

```yaml
---
- name: Loop Example
  hosts: all
  vars:
    names:
      - Ram
      - Shyam
      - John
    packages:
      - curl
      - wget
      - git
  tasks:
    - name: Print names using loop
      shell: echo "Hello {{ item }}"
      loop: "{{ names }}"
    
    - name: Install packages using loop
      apt:
        name: "{{ item }}"
        state: present
      loop: "{{ packages }}"
      become: yes
```

### Run Playbook

```bash
ansible-playbook -i inventory.ini loops-example.yaml
```

---

## Conditions

Execute tasks conditionally based on variables or facts.

### Create Playbook

```bash
nano condition-example.yaml
```

**condition-example.yaml content:**

```yaml
---
- name: Condition Example
  hosts: all
  vars:
    run_task: true
    environment: "production"
  tasks:
    - name: Run only if condition is true
      shell: echo "Condition matched"
      when: run_task

    - name: Run based on variable value
      shell: echo "Running in {{ environment }}"
      when: environment == "production"

    - name: Run if package is installed
      shell: echo "Git is installed"
      when: ansible_facts['packages']['git'] is defined
```

### Run Playbook

```bash
ansible-playbook -i inventory.ini condition-example.yaml
```

### Dry-run (Check Mode)

Preview changes without executing:

```bash
ansible-playbook -i inventory.ini condition-example.yaml -C
```

---

## Handlers

Handlers are tasks that only run when notified by other tasks, typically used for service restarts.

### Create Playbook

```bash
nano handlers-ex.yaml
```

**handlers-ex.yaml content:**

```yaml
---
- name: Handlers Example
  hosts: all
  tasks:
    - name: Execute shell command
      shell: echo "Task executed"
      notify:
        - Print Handler Message

    - name: Update configuration file
      shell: echo "Config updated"
      notify:
        - Restart Service

  handlers:
    - name: Print Handler Message
      shell: echo "Handler executed"

    - name: Restart Service
      shell: echo "Service restarted"
```

### Run Playbook

```bash
ansible-playbook -i inventory.ini handlers-ex.yaml
```

**Key Points:**
- Handlers only execute if notified by a task
- Handlers run at the end of the playbook, after all tasks
- Multiple tasks can notify the same handler
- Handler runs only once, even if notified multiple times

---

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `ansible -i inventory.ini webservers -m ping` | Test connectivity to all webservers |
| `ansible-playbook -i inventory.ini playbook.yaml` | Run a playbook |
| `ansible-playbook -i inventory.ini playbook.yaml -C` | Dry-run (check mode) |
| `ansible-playbook -i inventory.ini playbook.yaml -e "var=value"` | Run with runtime variables |
| `ansible-playbook -i inventory.ini playbook.yaml -v` | Verbose output |
| `ansible-playbook -i inventory.ini playbook.yaml -vv` | Very verbose output |
| `ansible all -i inventory.ini -m setup` | Gather facts from hosts |

---

## Tips & Best Practices

✅ **Do:**
- Use descriptive variable names
- Add comments to your playbooks
- Test with `-C` (check mode) before running
- Keep inventory files organized by environment
- Use handlers for service restarts

❌ **Don't:**
- Commit SSH keys to version control
- Use `become: yes` without necessity
- Hard-code sensitive information (use Ansible Vault)
- Run without testing in check mode first

---

## Troubleshooting

### Host Key Verification Failed
```bash
ssh-keyscan -H <IP_ADDRESS> >> ~/.ssh/known_hosts
```

### Permission Denied (SSH Key)
```bash
chmod 400 your-key.pem
```

### Playbook Syntax Error
```bash
ansible-playbook --syntax-check playbook.yaml
```

---

## References

- [Ansible Official Documentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/index.html)
- [Ansible Community](https://www.ansible.com/community)

---

**Last Updated:** May 2026
