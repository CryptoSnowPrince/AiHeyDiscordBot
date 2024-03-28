
# Discord bot

## Env

```
Python3 version: python3.10.12
pip3 version: 22.0.2
```

```
cp .env.example .env
```

```
update .env with new config
```

```
pip install -r requirements.txt
```

## dev mode

```
python3 bot.py
```

## product mode

```
pm2 start bot.py --name text2image-dc-bot --interpreter python3
```
```
pm2 stop bot.py
```
