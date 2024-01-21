# sendbot
A Bot For Delta.Chat to overtake sendmail and SMTP innings from scripts and WebApps

Bevor you can use the bot, you have to fill the to enviroment-variables with the Address and the Passwort of your bot. If you use an #chatmail-instance, make sure, that you added the address of this bot to the Part "# list of chatmail accounts which can send outbound un-encrypted mail
passthrough_senders =" and run ```./scripts/cmdeploy run``` in the chatmail-directory!



```
docker build -t sendbot .
docker compose up -d
```
To activate sendmail outside docker as a command, you can use this:

```
echo 'alias sendmail="docker exec -it sendbot python sendmail.py"' >> .bashrc
source .bashrc
```
You __may__ install senbot.py as a service an sendmail.py as a command with using
```
sudo scripts/install.sh
```
I don't think, it works very proper!
Please write a lot of issues!
