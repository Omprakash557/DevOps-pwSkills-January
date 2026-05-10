
# Ansible Setup on AWS EC2 Ubuntu - Complete Beginner Guide

## Prerequisites
- AWS EC2 instance running Ubuntu (t2.micro or larger)
- SSH access to your instance
- Basic terminal knowledge

---

## Step 1: Connect to Your EC2 Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

---

## Step 2: Update System Packages

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 3: Install Ansible

```bash
sudo apt install ansible -y
```

Verify installation:
```bash
ansible --version
```

---

## Step 4: Set Up Your Inventory File (Remote EC2 Instance)

Create an inventory file named `inventory.ini`:

```bash
nano inventory.ini
```

**Option 1: Using Public IP (Password-based - Not Recommended)**

```ini
[remote]
ec2-instance ansible_host=YOUR_EC2_PUBLIC_IP ansible_user=ubuntu ansible_password=your_password
```

**Option 2: Using Public IP with SSH Key (Recommended)**

```ini
[remote]
ec2-instance ansible_host=YOUR_EC2_PUBLIC_IP ansible_user=ubuntu ansible_ssh_private_key_file=/path/to/your-key.pem
```

**Example:**

```ini
[remote]
web-server ansible_host=54.123.456.789 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/my-key.pem
```

Replace:
- `54.123.456.789` with your EC2 **public IP address**
- `~/.ssh/my-key.pem` with path to your **PEM key file**

Save and exit (Ctrl+X, then Y, then Enter)

---

## Step 5: Test Connection to Remote EC2 Instance

Test if Ansible can connect to your remote EC2:

```bash
ansible -i inventory.ini remote -m ping
```

**Expected output:**
```
ec2-instance | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

If you see `"ping": "pong"` - Connection is working! ✅

---

## Common Issues:

**Issue: "Permission denied (publickey)"**
- Check PEM key path is correct
- Ensure key has correct permissions: `chmod 400 your-key.pem`

**Issue: "Connection timed out"**
- Check EC2 security group allows SSH (port 22)
- Verify public IP is correct
- Ensure EC2 instance is running

**Issue: "Host key verification failed"**
```bash
# Add this to inventory.ini:
[remote]
ec2-instance ansible_host=54.123.456.789 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/my-key.pem ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

---

## Step 7: Run Commands on Remote EC2

```bash
nano playbook.yml
```

```yaml
---
- name: Test
  hosts: local
  tasks:
    - shell: echo "Hello Ansible!"
    - shell: ls -la /home/ubuntu/
    - shell: echo "Test" > /tmp/test.txt
    - shell: whoami
```

Run it:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

---

## Step 8: More Useful Ansible Commands

### 1. Check Host Connectivity

```bash
# Ping single host
ansible -i inventory.ini remote -m ping

# Ping all hosts in inventory
ansible -i inventory.ini all -m ping

# Ping specific group
ansible -i inventory.ini remote -m ping
```

### 2. Get System Information

```bash
# Get all system facts (very long output)
ansible -i inventory.ini remote -m setup

# Get specific fact (OS family)
ansible -i inventory.ini remote -m setup -a "filter=ansible_os_family"

# Get specific fact (CPU cores)
ansible -i inventory.ini remote -m setup -a "filter=ansible_processor_vcpus"

# Get hostname
ansible -i inventory.ini remote -m setup -a "filter=ansible_hostname"
```

### 3. Run Shell Commands

```bash
# Simple echo
ansible -i inventory.ini remote -m shell -a "echo 'Hello World'"

# List directories
ansible -i inventory.ini remote -m shell -a "ls -la /home/ubuntu/"

# Check system uptime
ansible -i inventory.ini remote -m shell -a "uptime"

# Check disk space
ansible -i inventory.ini remote -m shell -a "df -h"

# Check memory usage
ansible -i inventory.ini remote -m shell -a "free -h"

# Check running processes
ansible -i inventory.ini remote -m shell -a "ps aux"

# Get network information
ansible -i inventory.ini remote -m shell -a "ip a"

# Check which user you are
ansible -i inventory.ini remote -m shell -a "whoami"

# Run multiple commands with pipe
ansible -i inventory.ini remote -m shell -a "df -h | head -2"
```

### 4. Package Management

```bash
# Install a package
ansible -i inventory.ini remote -m apt -a "name=curl state=present" -b

# Install multiple packages
ansible -i inventory.ini remote -m apt -a "name=git,curl,wget state=present" -b

# Remove a package
ansible -i inventory.ini remote -m apt -a "name=curl state=absent" -b

# Update package cache
ansible -i inventory.ini remote -m apt -a "update_cache=yes" -b

# Upgrade all packages
ansible -i inventory.ini remote -m apt -a "upgrade=full" -b

# Check if package is installed
ansible -i inventory.ini remote -m shell -a "dpkg -l | grep curl"
```

### 5. File Operations

```bash
# Create a file
ansible -i inventory.ini remote -m file -a "path=/tmp/test.txt state=touch"

# Create a directory
ansible -i inventory.ini remote -m file -a "path=/tmp/mydir state=directory"

# Delete a file
ansible -i inventory.ini remote -m file -a "path=/tmp/test.txt state=absent"

# Delete a directory
ansible -i inventory.ini remote -m file -a "path=/tmp/mydir state=absent"

# Change file permissions
ansible -i inventory.ini remote -m file -a "path=/tmp/test.txt mode=0755"

# Copy file
ansible -i inventory.ini remote -m copy -a "src=/tmp/test.txt dest=/tmp/test-copy.txt"

# Write content to file
ansible -i inventory.ini remote -m shell -a "echo 'Hello' > /tmp/hello.txt"
```

### 6. User Management

```bash
# Create a user
ansible -i inventory.ini remote -m user -a "name=newuser" -b

# Create user with home directory
ansible -i inventory.ini remote -m user -a "name=newuser state=present createhome=yes" -b

# Delete a user
ansible -i inventory.ini remote -m user -a "name=newuser state=absent" -b

# Add user to group
ansible -i inventory.ini remote -m user -a "name=newuser groups=sudo" -b

# List all users
ansible -i inventory.ini remote -m shell -a "cat /etc/passwd"
```

### 7. Service Management

```bash
# Start a service
ansible -i inventory.ini remote -m service -a "name=apache2 state=started" -b

# Stop a service
ansible -i inventory.ini remote -m service -a "name=apache2 state=stopped" -b

# Restart a service
ansible -i inventory.ini remote -m service -a "name=apache2 state=restarted" -b

# Enable service on boot
ansible -i inventory.ini remote -m service -a "name=apache2 enabled=yes" -b

# Check service status
ansible -i inventory.ini remote -m service -a "name=apache2 state=started" -b
```

### 8. Debug & Output

```bash
# Print simple message
ansible -i inventory.ini remote -m debug -a "msg='Hello World'"

# Print variable
ansible -i inventory.ini remote -m debug -a "msg='{{ ansible_hostname }}'"

# Show all facts
ansible -i inventory.ini remote -m debug -a "var=hostvars[inventory_hostname]"

# Verbose output
ansible-playbook -i inventory.ini playbook.yml -v

# Extra verbose output
ansible-playbook -i inventory.ini playbook.yml -vv

# Most verbose output
ansible-playbook -i inventory.ini playbook.yml -vvv
```

### 9. Playbook Commands

```bash
# Run a playbook
ansible-playbook -i inventory.ini playbook.yml

# Dry run (show what would happen, don't execute)
ansible-playbook -i inventory.ini playbook.yml --check

# Run with verbose output
ansible-playbook -i inventory.ini playbook.yml -v

# Check syntax without running
ansible-playbook -i inventory.ini playbook.yml --syntax-check

# Start playbook from specific task
ansible-playbook -i inventory.ini playbook.yml --start-at-task="Task Name"

# Run playbook with extra variables
ansible-playbook -i inventory.ini playbook.yml -e "var1=value1 var2=value2"

# List all tasks in playbook (dry run)
ansible-playbook -i inventory.ini playbook.yml --list-tasks

# Run playbook with tags
ansible-playbook -i inventory.ini playbook.yml --tags "tag1,tag2"

# Skip specific tags
ansible-playbook -i inventory.ini playbook.yml --skip-tags "tag1"
```

### 10. Inventory & Host Management

```bash
# List all hosts in inventory
ansible-inventory -i inventory.ini --list

# List hosts in specific group
ansible -i inventory.ini remote --list-hosts

# Show host info
ansible -i inventory.ini remote -m debug -a "msg='{{ inventory_hostname }}'"

# Count hosts in inventory
ansible -i inventory.ini all --list-hosts | wc -l

# Get host variables
ansible -i inventory.ini remote -m debug -a "var=hostvars[inventory_hostname]"
```

### 11. Useful Modifiers (Flags)

```bash
# -b or --become : Run with sudo
ansible-playbook -i inventory.ini playbook.yml -b

# -u or --user : Specify SSH user
ansible -i inventory.ini remote -u ubuntu -m ping

# -k : Ask for password
ansible-playbook -i inventory.ini playbook.yml -k

# -K : Ask for sudo password
ansible-playbook -i inventory.ini playbook.yml -K

# --limit : Run on specific hosts only
ansible-playbook -i inventory.ini playbook.yml --limit remote

# --extra-vars : Pass variables
ansible-playbook -i inventory.ini playbook.yml -e "myvar=value"

# --diff : Show changes made
ansible-playbook -i inventory.ini playbook.yml --diff

# --check : Dry run mode
ansible-playbook -i inventory.ini playbook.yml --check
```

### 12. Example Combinations

```bash
# Run playbook on all hosts with verbose output and dry-run
ansible-playbook -i inventory.ini playbook.yml -v --check

# Run specific group with become (sudo) and show changes
ansible-playbook -i inventory.ini playbook.yml -b --diff --limit remote

# Run with extra variables and verbose
ansible-playbook -i inventory.ini playbook.yml -e "env=prod" -vv

# Dry run with syntax check
ansible-playbook -i inventory.ini playbook.yml --syntax-check --check

# Run from specific task with verbose output
ansible-playbook -i inventory.ini playbook.yml --start-at-task="Install Packages" -v
```

---

### Test Connection Methods:

```bash
# Method 1: Ping test (most common)
ansible -i inventory.ini remote -m ping

# Method 2: Check if host is reachable
ansible -i inventory.ini remote -m debug -a "msg='Connected!'"

# Method 3: Run a simple command
ansible -i inventory.ini remote -m shell -a "echo 'Testing Ansible'"

# Method 4: Get system facts
ansible -i inventory.ini remote -m setup | head -20

# Method 5: Check Ansible version on target
ansible -i inventory.ini remote -m debug -a "msg='{{ ansible_version }}'"
```

### Other Ad-hoc Examples:

```bash
# Check current user
ansible -i inventory.ini remote -m shell -a "whoami"

# List files
ansible -i inventory.ini remote -m shell -a "ls -la /home/ubuntu/"

# Check disk space
ansible -i inventory.ini remote -m shell -a "df -h"

# Run any bash command
ansible -i inventory.ini remote -m shell -a "free -h"
```

---

## Step 9: Project Structure (Best Practice)

Organize your project like this:

```
ansible-project/
├── inventory.ini
├── first-playbook.yml
├── basic-tasks.yml
└── playbooks/
    └── more-playbooks.yml
```

---

## Common Issues & Fixes

**Issue: Permission denied errors**
- Solution: Add `become: yes` to tasks that need sudo
- Or run playbook with: `ansible-playbook -i inventory.ini playbook.yml -b`

**Issue: "ansible: command not found"**
- Solution: Reinstall: `sudo apt install ansible -y`

**Issue: Playbook won't run**
- Solution: Check YAML syntax (spaces matter!)
- Use online YAML validators

---

## Next Steps

1. **Learn more modules**: Visit [Ansible Modules Documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html)

2. **Create variables**: Use `vars:` section in playbooks

3. **Use handlers**: Trigger tasks only when changes occur

4. **Run multiple hosts**: Add more hosts to inventory file

5. **Create roles**: Organize complex playbooks into reusable roles

---

## Quick Reference Commands

```bash
# Run a playbook
ansible-playbook -i inventory.ini playbook.yml

# Run playbook with verbose output
ansible-playbook -i inventory.ini playbook.yml -v

# Run specific task only (by name)
ansible-playbook -i inventory.ini playbook.yml --start-at-task "Task Name"

# Test syntax without running
ansible-playbook -i inventory.ini playbook.yml --syntax-check

# Run ad-hoc command
ansible -i inventory.ini local -m command -a "your-command"

# Gather system facts
ansible -i inventory.ini local -m setup
```

---

## Summary

✅ Installed Ansible on EC2  
✅ Created inventory file with localhost  
✅ Wrote and ran your first playbook  
✅ Learned basic tasks (file, copy, debug, command)  
✅ Explored ad-hoc commands  

You now have a working Ansible setup! Start small and explore more tasks as needed.
