# 🚀 Ansible – Create EC2 Instance (Ubuntu t3.micro)

Launch an Ubuntu EC2 instance on AWS using Ansible — runs locally via WSL on Windows.

---

## 📁 Files

### `create_ec2.yaml`
```yaml
---
- name: Create EC2 Instance
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    aws_access_key: YOUR_ACCESS_KEY
    aws_secret_key: YOUR_SECRET_KEY
    aws_region: us-east-1

  tasks:
    - name: Launch Ubuntu t3.micro
      amazon.aws.ec2_instance:
        access_key: "{{ aws_access_key }}"
        secret_key: "{{ aws_secret_key }}"
        region: "{{ aws_region }}"
        name: my-ubuntu-server
        instance_type: t3.micro
        image_id: ami-0fc5d935ebf8bc3bc   # Ubuntu 22.04 LTS (us-east-1)
        state: running
        wait: true
      register: ec2

    - name: Show instance details
      debug:
        msg:
          - "Instance ID : {{ ec2.instances[0].instance_id }}"
          - "Public IP   : {{ ec2.instances[0].public_ip_address | default('N/A') }}"
```

### `inventory.ini`
```ini
[local]
localhost ansible_connection=local
```

---

## 🪟 Installing Ansible on Windows (via WSL)

**Step 1 — Open WSL**

**Step 2 — Install Ansible**
```bash
sudo apt update
sudo apt install software-properties-common python3-pip
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
ansible --version
```

---

## ☁️ Installing AWS CLI on Ubuntu / WSL

```bash
sudo apt install unzip curl -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

---

## 🔑 Configure AWS Credentials

```bash
aws configure
```

| Prompt | Value |
|--------|-------|
| Access Key | your access key |
| Secret Key | your secret key |
| Region | `ap-south-1` |
| Format | `json` |

---

## 📝 Create the Playbook Files

```bash
nano create_ec2.yaml   # paste the content above
nano inventory.ini     # paste the content above
```

---

## ✅ Before Running — Checklist

| # | What to verify |
|---|----------------|
| 1 | `ami_id` is correct for your region |
| 2 | `aws_region` matches your target region |
| 3 | `aws_access_key` and `aws_secret_key` are filled in |
| 4 | Instance `name` is set (make it unique!) |

---

## ▶️ Run the Playbook

```bash
ansible-playbook create_ec2.yaml
```

For verbose output:
```bash
ansible-playbook create_ec2.yaml -v
```
