<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://socialify.git.ci/TTB-Network/python-openbmclapi-v2/image?description=1&font=Inter&language=1&logo=https%3A%2F%2Fpython-openbmclapi.bugungu.top%2Fimg%2Flogo.svg&name=1&owner=1&pattern=Plus&theme=Dark">
  <source media="(prefers-color-scheme: light)" srcset="https://socialify.git.ci/TTB-Network/python-openbmclapi-v2/image?description=1&font=Inter&language=1&logo=https%3A%2F%2Fpython-openbmclapi.bugungu.top%2Fimg%2Flogo.svg&name=1&owner=1&pattern=Plus&theme=Light">
  <img src="https://socialify.git.ci/TTB-Network/python-openbmclapi-v2/image?description=1&font=Inter&language=1&logo=https%3A%2F%2Fpython-openbmclapi.bugungu.top%2Fimg%2Flogo.svg&name=1&owner=1&pattern=Plus&theme=Auto">
</picture>

# OpenBMCLAPI for Python v2

🥳 热烈祝贺 python-openbmclapi v2 的发布！🥳

简体中文 | [English](/i18n/README_en.md)

![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/TTB-Network/python-openbmclapi-v2)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/TTB-Network/python-openbmclapi-v2)
![GitHub License](https://img.shields.io/github/license/TTB-Network/python-openbmclapi-v2)
![GitHub Release](https://img.shields.io/github/v/release/TTB-Network/python-openbmclapi-v2)
![GitHub Tag](https://img.shields.io/github/v/tag/TTB-Network/python-openbmclapi-v2)
![Docker Pulls](https://img.shields.io/docker/pulls/silianz/python-openbmclapi-v2)
[![Crowdin](https://badges.crowdin.net/python-openbmclapi-site/localized.svg)](https://crowdin.com/project/python-openbmclapi-site)
![GitHub Repo stars](https://img.shields.io/github/stars/TTB-Network/python-openbmclapi-v2)
[![CodeQL](https://github.com/TTB-Network/python-openbmclapi-v2/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/TTB-Network/python-openbmclapi-v2/actions/workflows/github-code-scanning/codeql)
[![Create tagged release](https://github.com/TTB-Network/python-openbmclapi-v2/actions/workflows/build_and_publish.yml/badge.svg)](https://github.com/TTB-Network/python-openbmclapi-v2/actions/workflows/build_and_publish.yml)

[文档](https://python-openbmclapi.bugungu.top/) | [API](https://python-openbmclapi.bugungu.top/docs/api) | [赞助](https://afdian.net/a/bugungu)

✨ 基于 [OpenBMCLAPI](https://github.com/bangbang93/openbmclapi) 的 Python 实现。

🎨 **跨系统**、**跨架构**。这得益于 Python 强大的语言功能。

✨ **Docker** 支持。通过 Docker 更加**快捷地**部署 python-openbmclapi ~~（更支持一键跑路）~~。

🎉 __*新增功能！*__ 仪表盘。我们使用了 Vue.js 和前端请求（axios）等功能使得新一代仪表盘界面更加简洁。

</div>

## 目录

- [简介](#简介)
- [核心特性](#核心特性)
- [快速开始](#快速开始)
  - [前置要求](#前置要求)
  - [安装步骤](#安装步骤)
  - [Docker 部署](#docker-部署)
- [配置说明](#配置说明)
  - [基础配置](#基础配置)
  - [存储配置](#存储配置)
- [贡献](#贡献)
- [鸣谢](#鸣谢)

## 简介

本项目是 [OpenBMCLAPI](https://github.com/bangbang93/openbmclapi) 的 Python 版本，OpenBMCLAPI 是通过分布式集群帮助 [BMCLAPI](https://bmclapidoc.bangbang93.com/) 进行文件分发、加速中国大陆 Minecraft 下载的公益项目。

如果你想加入 OpenBMCLAPI，可以寻找 [bangbang93](https://github.com/bangbang93) 获取 `CLUSTER_ID` 和 `CLUSTER_SECRET`。

## 核心特性

### 🎯 多存储后端支持

- **本地存储** - 传统的本地文件系统存储
- **AList** - 支持通过 AList 进行文件管理和分发
- **S3 兼容存储** - 支持 AWS S3、MinIO、阿里云 OSS 等 S3 兼容的对象存储服务

### 📊 实时监控仪表盘

- 实时性能监控（CPU、内存、连接数）
- 多维度请求统计（小时/天/月）
- 用户分布可视化
- 响应式设计，支持移动设备访问

### 🚀 高性能架构

- 异步 I/O 处理，提高并发性能
- 智能文件同步机制
- 自动回收过期文件
- 支持断点续传

### 🌍 国际化支持

- 多语言界面支持
- 通过 Crowdin 协作翻译

## 快速开始

### 前置要求

- Python 3.12 或更高版本
- pip 包管理器
- （可选）Docker 和 Docker Compose

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/TTB-Network/python-openbmclapi-v2.git
cd python-openbmclapi-v2
```

2. **安装依赖**

```bash
pip install -r requirements.txt
# 或使用 Poetry
poetry install
```

3. **配置应用**

编辑 `config/config.yml` 文件，填入你的集群配置：

```yaml
cluster:
  id: "你的集群ID"
  secret: "你的集群密钥"
  host: "你的域名或IP"
  port: 8800
```

4. **启动应用**

```bash
python main.py
```

### Docker 部署

使用 Docker 是最简单的部署方式：

```bash
docker run -d \
  --name python-openbmclapi \
  -p 8800:8800 \
  -v /path/to/cache:/app/cache \
  -v /path/to/config:/app/config \
  silianz/python-openbmclapi-v2:latest
```

或使用 Docker Compose：

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

## 配置说明

### 基础配置

配置文件位于 `config/config.yml`：

```yaml
cluster:
  base_url: "https://openbmclapi.bangbang93.com"  # 主控地址
  id: ""                    # 集群 ID
  secret: ""                # 集群密钥
  host: ""                  # 公网访问地址
  byoc: false               # 是否使用自己的证书
  public_port: -1           # 公网端口（-1 表示使用 port）
  port: 8800                # 监听端口

advanced:
  lang: "zh_cn"             # 语言设置
  debug: false              # 调试模式
  retry: 5                  # 重试次数
  delay: 15                 # 重试延迟（秒）
  keep_alive: 60            # 保活间隔（秒）
  sync_interval: 120        # 同步间隔（秒）
```

### 存储配置

支持配置多个存储后端，系统会依次尝试从各存储读取文件：

#### 本地存储

```yaml
storages:
  - type: "local"
    path: "./cache"
```

#### AList 存储

```yaml
storages:
  - type: "alist"
    url: "http://your-alist-server.com"
    username: "admin"
    password: "password"
    path: "/openbmclapi/"
```

#### S3 兼容存储

```yaml
storages:
  - type: "s3"
    endpoint: "https://s3.amazonaws.com"      # S3 端点地址
    access_key_id: "your-access-key"          # 访问密钥 ID
    secret_access_key: "your-secret-key"      # 访问密钥
    bucket: "your-bucket-name"                # 存储桶名称
    signature_version: "s3v4"                 # 签名版本（可选）
    addressing_style: "auto"                  # 寻址样式：auto/path/virtual（可选）
    session_token: null                       # 会话令牌（可选）
```

**S3 配置说明：**

- `endpoint`: S3 服务端点
  - AWS S3: `https://s3.amazonaws.com` 或区域端点如 `https://s3.us-west-2.amazonaws.com`
  - MinIO: `http://your-minio-server:9000`
  - 阿里云 OSS: `https://oss-cn-hangzhou.aliyuncs.com`
- `signature_version`: 签名版本，通常使用 `s3v4`
- `addressing_style`: 
  - `auto`: 自动选择
  - `path`: 路径样式（`endpoint/bucket/key`）
  - `virtual`: 虚拟主机样式（`bucket.endpoint/key`）

## 贡献

如果你有能力，你可以向我们的仓库提交 Pull Request 或 Issue。

如果你想帮助我们进行多语言翻译，请前往 [Crowdin](https://translate.bugungu.top)。

在贡献之前，请先阅读我们的[贡献准则](./CONTRIBUTING.md)。

## 鸣谢

感谢以下项目为本项目提供的灵感和参考：

- [LiterMC/go-openbmclapi](https://github.com/LiterMC/go-openbmclapi)
- [bangbang93/openbmclapi](https://github.com/bangbang93/openbmclapi)
- [SALTWOOD/CSharp-OpenBMCLAPI](https://github.com/SALTWOOD/CSharp-OpenBMCLAPI)
