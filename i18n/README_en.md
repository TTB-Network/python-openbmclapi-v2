<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://socialify.git.ci/TTB-Network/python-openbmclapi/image?description=1&font=Inter&language=1&logo=https%3A%2F%2Fpython-openbmclapi.ttb-network.top%2Fimg%2Flogo.svg&name=1&owner=1&pattern=Plus&theme=Dark">
  <source media="(prefers-color-scheme: light)" srcset="https://socialify.git.ci/TTB-Network/python-openbmclapi/image?description=1&font=Inter&language=1&logo=https%3A%2F%2Fpython-openbmclapi.ttb-network.top%2Fimg%2Flogo.svg&name=1&owner=1&pattern=Plus&theme=Light">
  <img src="https://socialify.git.ci/TTB-Network/python-openbmclapi/image?description=1&font=Inter&language=1&logo=https%3A%2F%2Fpython-openbmclapi.ttb-network.top%2Fimg%2Flogo.svg&name=1&owner=1&pattern=Plus&theme=Auto">
</picture>

# OpenBMCLAPI for Python v2

[简体中文](/README.md) | English

![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/TTB-Network/python-openbmclapi)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/TTB-Network/python-openbmclapi)
![GitHub License](https://img.shields.io/github/license/TTB-Network/python-openbmclapi)
![GitHub Release](https://img.shields.io/github/v/release/TTB-Network/python-openbmclapi)
![GitHub Tag](https://img.shields.io/github/v/tag/TTB-Network/python-openbmclapi)
![Docker Pulls](https://img.shields.io/docker/pulls/silianz/python-openbmclapi)
[![Crowdin](https://badges.crowdin.net/python-openbmclapi-site/localized.svg)](https://crowdin.com/project/python-openbmclapi-site)
![GitHub Repo stars](https://img.shields.io/github/stars/TTB-Network/python-openbmclapi)
[![CodeQL](https://github.com/TTB-Network/python-openbmclapi/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/TTB-Network/python-openbmclapi/actions/workflows/github-code-scanning/codeql)
[![Create tagged release](https://github.com/TTB-Network/python-openbmclapi/actions/workflows/build_and_publish.yml/badge.svg)](https://github.com/TTB-Network/python-openbmclapi/actions/workflows/build_and_publish.yml)

[Docs](https://python-openbmclapi.ttb-network.top/) | [API](https://python-openbmclapi.ttb-network.top/docs/api) | [Sponsorship](https://afdian.net/a/atianxiua)

✨ Python implementation based on [OpenBMCLAPI](https://github.com/bangbang93/openbmclapi).

🎨 **Cross-platform** and **cross-architecture**. Thanks to the powerful features of Python.

✨ **Docker** support. Deploy python-openbmclapi quickly with Docker.

🎉 **New Feature!** Dashboard. Built with Vue.js for a modern, clean interface.

</div>

## Table of Contents

- [Introduction](#introduction)
- [Core Features](#core-features)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Docker Deployment](#docker-deployment)
- [Configuration](#configuration)
  - [Basic Configuration](#basic-configuration)
  - [Storage Configuration](#storage-configuration)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Introduction

This project is a Python version of [OpenBMCLAPI](https://github.com/bangbang93/openbmclapi). OpenBMCLAPI is a file distribution cluster that helps [BMCLAPI](https://bmclapidoc.bangbang93.com/) accelerate Minecraft downloads in mainland China.

If you want to join OpenBMCLAPI, contact [bangbang93](https://github.com/bangbang93) to obtain a `CLUSTER_ID` and `CLUSTER_SECRET`.

## Core Features

### 🎯 Multiple Storage Backend Support

- **Local Storage** - Traditional local filesystem storage
- **AList** - File management and distribution through AList
- **S3-Compatible Storage** - Support for AWS S3, MinIO, Alibaba Cloud OSS, and other S3-compatible object storage services

### 📊 Real-time Monitoring Dashboard

- Real-time performance monitoring (CPU, memory, connections)
- Multi-dimensional request statistics (hourly/daily/monthly)
- User distribution visualization
- Responsive design with mobile device support

### 🚀 High-Performance Architecture

- Asynchronous I/O processing for better concurrency
- Smart file synchronization mechanism
- Automatic cleanup of expired files
- Resume download support

### 🌍 Internationalization Support

- Multi-language interface
- Collaborative translation via Crowdin

## Quick Start

### Prerequisites

- Python 3.12 or higher
- pip package manager
- (Optional) Docker and Docker Compose

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/TTB-Network/python-openbmclapi-v2.git
cd python-openbmclapi-v2
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
# Or using Poetry
poetry install
```

3. **Configure the application**

Edit `config/config.yml` and fill in your cluster configuration:

```yaml
cluster:
  id: "your-cluster-id"
  secret: "your-cluster-secret"
  host: "your-domain-or-ip"
  port: 8800
```

4. **Start the application**

```bash
python main.py
```

### Docker Deployment

Using Docker is the easiest way to deploy:

```bash
docker run -d \
  --name python-openbmclapi \
  -p 8800:8800 \
  -v /path/to/cache:/app/cache \
  -v /path/to/config:/app/config \
  silianz/python-openbmclapi-v2:latest
```

Or use Docker Compose:

```yaml
version: '3'
services:
  openbmclapi:
    image: silianz/python-openbmclapi-v2:latest
    ports:
      - "8800:8800"
    volumes:
      - ./cache:/app/cache
      - ./config:/app/config
    restart: unless-stopped
```

## Configuration

### Basic Configuration

Configuration file located at `config/config.yml`:

```yaml
cluster:
  base_url: "https://openbmclapi.bangbang93.com"  # Master server URL
  id: ""                    # Cluster ID
  secret: ""                # Cluster secret
  host: ""                  # Public access address
  byoc: false               # Bring your own certificate
  public_port: -1           # Public port (-1 uses port value)
  port: 8800                # Listening port

advanced:
  lang: "zh_cn"             # Language setting
  debug: false              # Debug mode
  retry: 5                  # Retry count
  delay: 15                 # Retry delay (seconds)
  keep_alive: 60            # Keep-alive interval (seconds)
  sync_interval: 120        # Sync interval (seconds)
```

### Storage Configuration

Support multiple storage backends. The system will try to read files from each storage in sequence:

#### Local Storage

```yaml
storages:
  - type: "local"
    path: "./cache"
```

#### AList Storage

```yaml
storages:
  - type: "alist"
    url: "http://your-alist-server.com"
    username: "admin"
    password: "password"
    path: "/openbmclapi/"
```

#### S3-Compatible Storage

```yaml
storages:
  - type: "s3"
    endpoint: "https://s3.amazonaws.com"      # S3 endpoint URL
    access_key_id: "your-access-key"          # Access key ID
    secret_access_key: "your-secret-key"      # Secret access key
    bucket: "your-bucket-name"                # Bucket name
    signature_version: "s3v4"                 # Signature version (optional)
    addressing_style: "auto"                  # Addressing style: auto/path/virtual (optional)
    session_token: null                       # Session token (optional)
```

**S3 Configuration Details:**

- `endpoint`: S3 service endpoint
  - AWS S3: `https://s3.amazonaws.com` or regional endpoint like `https://s3.us-west-2.amazonaws.com`
  - MinIO: `http://your-minio-server:9000`
  - Alibaba Cloud OSS: `https://oss-cn-hangzhou.aliyuncs.com`
- `signature_version`: Signature version, usually `s3v4`
- `addressing_style`: 
  - `auto`: Automatic selection
  - `path`: Path-style (`endpoint/bucket/key`)
  - `virtual`: Virtual-hosted-style (`bucket.endpoint/key`)

## Contributing

If you have the ability, you can submit a Pull Request or Issue to our repository.

If you want to help us with multilingual translations, go to [Crowdin](https://translate.bugungu.top).

Please read our [Contributing Rules](./CONTRIBUTING_en.md) before contributing.

## Acknowledgments

Thanks to the following projects for inspiration and reference:

- [LiterMC/go-openbmclapi](https://github.com/LiterMC/go-openbmclapi)
- [bangbang93/openbmclapi](https://github.com/bangbang93/openbmclapi)
- [SALTWOOD/CSharp-OpenBMCLAPI](https://github.com/SALTWOOD/CSharp-OpenBMCLAPI)
