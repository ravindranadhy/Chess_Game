# Chess AI Project

An AI-powered chess game using Python with `python-chess` for game logic and `Pygame` for the GUI.

## Setup Instructions

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `chess_ai.py` - Main AI engine with Minimax algorithm
- `chess_gui.py` - Pygame-based graphical interface
- `main.py` - Game loop and integration

## How to Run

```bash
python main.py
```

## Features

- Complete chess rules implementation (castling, en passant, pawn promotion)
- AI using Minimax with Alpha-Beta pruning
- Interactive GUI with drag-and-drop piece movement
- Move validation and game state detection (check, checkmate, stalemate)




docker --version
docker login
docker images
docker image ls
docker ps
docker ps -a
docker pull redis
docker run redis
docker run --name myredis -d redis
docker run -d -p 8081:8080 --name mycontainer myimage
docker stop myredis
docker start myredis
docker restart myredis
docker rm myredis
docker rmi redis
docker exec -it myredis redis-cli
docker exec -it mycontainer bash
docker logs mycontainer
docker inspect mycontainer
docker stats
docker build -t myimage .
docker tag myimage username/myimage:latest
docker push username/myimage:latest
docker pull username/myimage:latest
docker commit mycontainer username/myimage
docker logout


git --version
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global user.name
git config --global user.email
git init
git status
git add .
git add filename
git commit -m "first commit"
git log
git log --oneline
git log --oneline --all --decorate
git branch
git branch feature
git checkout feature
git checkout main
git checkout -b feature
git merge feature
git revert <commit-hash>
git stash
git stash -u
git stash list
git stash pop
git restore filename
git diff
git diff --staged
git remote -v
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY.git
git remote set-url origin https://github.com/YOUR_USERNAME/REPOSITORY.git
git branch -M main
git push -u origin main
git push
git pull
git fetch
git clone https://github.com/USERNAME/REPOSITORY.git
git rm filename
git mv oldname newname
