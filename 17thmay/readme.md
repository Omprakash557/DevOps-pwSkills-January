# Ansible Apache Role

A complete Ansible role to automate Apache2 installation and configuration on Ubuntu EC2 instances. This project demonstrates infrastructure-as-code best practices using Ansible roles and playbooks.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Role Components](#role-components)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This Ansible role automates the following tasks on Ubuntu systems:

- Install Apache2 web server
- Start and enable Apache2 service
- Deploy a custom HTML homepage
- Manage service restarts through handlers

Perfect for:
- Quick web server provisioning
- Learning Ansible roles and best practices
- CI/CD pipeline integration
- Infrastructure automation

## 📦 Prerequisites

### System Requirements

- **OS**: Ubuntu 20.04 LTS or later
- **Instance Type**: AWS EC2 t3.micro or equivalent
- **Security Group**: HTTP (80) and HTTPS (443) ports enabled
- **IAM Permissions**: EC2 access

### Software Requirements

- Ansible 2.9+
- Python 3.6+
- SSH access to target machines
- `sudo` privileges on target hosts

## 🗂️ Project Structure

```
ansible-apache-role/
├── apache_role/
│   ├── defaults/          # Default variables
│   ├── files/             # Static files
│   ├── handlers/          # Event handlers
│   │   └── main.yml       # Handler definitions
│   ├── meta/              # Role metadata
│   ├── tasks/             # Main role tasks
│   │   └── main.yml       # Task definitions
│   ├── templates/         # Jinja2 templates
│   │   └── index.html.j2  # Custom webpage template
│   ├── tests/             # Test files
│   └── vars/              # Role variables
├── inventory.ini          # Host inventory
├── site.yml               # Main playbook
└── README.md              # This file
```

## 🚀 Installation & Setup

### Step 1: Launch EC2 Instance

```bash
# AWS Console: Launch EC2 instance
# - AMI: Ubuntu Server 22.04 LTS
# - Instance Type: t3.micro
# - Security Group: Allow HTTP (80) & HTTPS (443)
```

### Step 2: Install Ansible

```bash
# Update package manager
sudo apt update

# Install Ansible
sudo apt install ansible -y

# Verify installation
ansible --version
```

### Step 3: Create Project Directory

```bash
# Create and navigate to project directory
mkdir ansible-apache-role
cd ansible-apache-role
```

### Step 4: Create Inventory File

```bash
# Create inventory
nano inventory.ini
```

Paste the following content:

```ini
[webservers]
localhost ansible_connection=local
```

### Step 5: Verify Ansible Connectivity

```bash
# Test connection to all hosts
ansible -i inventory.ini webservers -m ping
```

Expected output:
```
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### Step 6: Initialize Role Structure

```bash
# Create role using Ansible Galaxy
ansible-galaxy init apache_role

# Navigate to project root
cd ..
```

## 📝 Configuration

### Task 1: Create Tasks File

```bash
nano apache_role/tasks/main.yml
```

Add the following content:

```yaml
---
- name: Install Apache2
  apt:
    name: apache2
    state: present
    update_cache: yes

- name: Start Apache2
  service:
    name: apache2
    state: started
    enabled: yes

- name: Copy custom webpage
  template:
    src: index.html.j2
    dest: /var/www/html/index.html
  notify: Restart Apache2
```

### Task 2: Create HTML Template

```bash
nano apache_role/templates/index.html.j2
```

Add the following content:

```html
<html>
<head>
    <title>Ansible Apache Demo</title>
</head>
<body>
    <h1>Apache Installed using Ansible Role</h1>
    <h2>Hello from AWS EC2</h2>
</body>
</html>
```

### Task 3: Create Handlers

```bash
nano apache_role/handlers/main.yml
```

Add the following content:

```yaml
---
- name: Restart Apache2
  service:
    name: apache2
    state: restarted
```

### Task 4: Create Main Playbook

```bash
nano site.yml
```

Add the following content:

```yaml
---
- name: Install Apache using Role
  hosts: webservers
  become: yes
  roles:
    - apache_role
```

## 🎮 Usage

### Run the Playbook

```bash
# Execute the playbook
ansible-playbook -i inventory.ini site.yml
```

### Verbose Output

For detailed execution information:

```bash
# Show verbose output (more details)
ansible-playbook -i inventory.ini site.yml -v

# Show very verbose output (task-level details)
ansible-playbook -i inventory.ini site.yml -vv

# Show debug output (variable values)
ansible-playbook -i inventory.ini site.yml -vvv
```

### Dry Run (Check Mode)

Test changes without applying them:

```bash
ansible-playbook -i inventory.ini site.yml --check
```

### Specific Tags

Run only specific tasks:

```bash
ansible-playbook -i inventory.ini site.yml --tags "install"
```

## 🔧 Role Components

### Tasks (`apache_role/tasks/main.yml`)

- **Install Apache2**: Uses `apt` module to install Apache2 package
- **Start Service**: Enables and starts Apache2 service
- **Deploy Webpage**: Uses Jinja2 template to deploy custom HTML

### Handlers (`apache_role/handlers/main.yml`)

- **Restart Apache2**: Triggered when webpage is updated

### Templates (`apache_role/templates/`)

- **index.html.j2**: Custom homepage with dynamic content support

### Inventory (`inventory.ini`)

Defines target hosts and connection methods:
```ini
[webservers]
localhost ansible_connection=local
```

### Playbook (`site.yml`)

Main orchestration file that applies the role to webserver group.

## ✅ Verification

After running the playbook, verify the installation:

```bash
# Check if Apache is running
sudo systemctl status apache2

# Test HTTP connectivity
curl http://localhost

# Check Apache version
apache2 -v
```

Expected response: Your custom HTML webpage should display.

## 🔍 Troubleshooting

### Issue: Permission Denied

```bash
# Solution: Ensure user has sudo access
sudo usermod -aG sudo $USER
```

### Issue: Ansible Command Not Found

```bash
# Solution: Reinstall Ansible
sudo apt remove ansible -y
sudo apt install ansible -y
```

### Issue: Apache Port Already in Use

```bash
# Solution: Check what's using port 80
sudo lsof -i :80

# Kill the process if needed
sudo kill -9 <PID>
```

### Issue: Playbook Fails with Connection Error

```bash
# Solution: Verify inventory connectivity
ansible -i inventory.ini webservers -m ping -vv

# Check SSH keys if using remote hosts
ssh-keygen -t rsa -N ""
```

### Issue: Template Not Found

```bash
# Solution: Verify file structure
ls -la apache_role/templates/
ls -la apache_role/tasks/
```

## 📚 Learning Resources

- [Ansible Official Documentation](https://docs.ansible.com/)
- [Ansible Roles Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
- [Jinja2 Template Engine](https://jinja.palletsprojects.com/)
- [Ubuntu Apache2 Documentation](https://ubuntu.com/server/docs/web-servers-apache)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created as a demonstration of Ansible role best practices for infrastructure automation.

## 💬 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section above

---

**Happy Automating! 🚀**

Last Updated: May 2026
