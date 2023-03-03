
# Discord bot
```
cp .env.example .env
```
```
update .env with new config
```
```
pip install -r requirements.txt
```
### dev mode
```
python3 bot.py
```
### product mode
```
pm2 start bot.py --name aiheydicordbot --interpreter python3
```
```
pm2 stop bot.py
```
