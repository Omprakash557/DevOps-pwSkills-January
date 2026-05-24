# 🐳 Docker Setup & Command Reference

A beginner-friendly guide to installing Docker on Ubuntu and getting started with essential commands.

---

## 📦 Installation

### 1. Update & Install Prerequisites

```bash
sudo apt update
sudo apt install ca-certificates curl gnupg
```

### 2. Set Up Docker's GPG Key

```bash
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### 3. Add Docker Repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 4. Install Docker Engine

```bash
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 5. Verify Installation

```bash
sudo systemctl status docker
```

---

## 🛠️ Essential Commands

### Switch to Root

```bash
sudo -i
```

### Image Management

```bash
# List all downloaded images
docker images

# Pull an image from Docker Hub
docker pull ubuntu
```

### Container Management

```bash
# List all containers (running + stopped)
# ps = process, -a = all
docker ps -a

# Run a container interactively with a custom name
docker run -it --name vadapav ubuntu
# --name vadapav  →  assigns the name "vadapav" to the running container
# ubuntu          →  the image used to create the container
```

---

## 🧪 Hands-On Demo — Inside a Container

Once inside the container shell, try these:

```bash
# Create some directories
mkdir test
mkdir prod

# Update package lists
apt-get update

# Install figlet (ASCII art text tool)
apt-get install figlet

# Try it out!
figlet docker

# Exit the container
exit
```

> **💡 Why does `command not found` appear inside a container?**
> Docker containers are minimal by default — they ship with only the bare essentials.
> Common tools like `figlet`, `curl`, or even `ping` won't exist until you explicitly install them with `apt-get install`.

---

## 🗂️ Quick Reference

| Command | Description |
|---|---|
| `docker images` | List all local images |
| `docker pull <image>` | Download an image from Docker Hub |
| `docker ps -a` | List all containers |
| `docker run -it --name <name> <image>` | Run a container interactively |
| `docker start <name>` | Start a stopped container |
| `docker stop <name>` | Stop a running container |
| `docker rm <name>` | Remove a container |
| `docker rmi <image>` | Remove an image |

---

## 📚 Resources

- [Docker Official Docs](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Install Docker on Ubuntu (Official Guide)](https://docs.docker.com/engine/install/ubuntu/)
