# Hitchhiking Diary Server

FastAPI-powered server service for the iOS application for documenting hitchhiking travels. Designed to effortlessly
synchronize your hitchhiking adventures across your family and friends so they know you are safe.

**Work in progress**

## Features

- [X] **Mobile App Sync**: Synchronization services for [hitchhiking-diary-ios](https://github.com/Sibyx/hitchhiking-diary-ios/)
- [X] **Public dashboard**: Public dashboard to share your journey with your friends and family!
- [ ] **Story generator**: Image generator for Instagram stories for each day

## Getting Started

### From scratch

```shell
# Clone the repository
git clone git@github.com:Sibyx/hitchhiking-diary-server.git hitchhiking-diary-server

# Create environment and install dependencies
cd hitchhiking-diary-server
python -m venv .venv
source .venv/bin/active
poetry install

# Create configuration (edit the .env)
cp .env.example .env

# Run server
uvicorn main:app --reload
```

## CLI

The server comes with some CLI to easy setup and maintenance:

| Command                                              | Description        |
|------------------------------------------------------|--------------------|
| `python -m hitchhiking_diary_server.cli create-user` | Creates a new user |

---
If you enjoy using this project, consider donating! Your donations will go towards therapy sessions because
I'm an alcoholic and substance abuser and this is my cry for help. Cheers 🍻!
