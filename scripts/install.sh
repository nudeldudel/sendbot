#!/usr/bin/bash
cp sendbot.py /usr/local/bin/sendbot.py
chmod +x /usr/local/bin/sendbot.py
useradd -r -s /bin/false sendbot
mkdir /etc/sendbot && chown -R sendbot:sendbot /etc/sendbot
PPATH=$(sudo -u sendbot which python3)
echo "PPATH=$PPATH" > /etc/sendbot/sendbot.conf
echo "DELTACHAT_HOST=localhost" >> /etc/sendbot/sendbot.conf
echo "DELTACHAT_PORT=8025" >> /etc/sendbot/sendbot.conf
echo "DELTACHAT_DB_PATH=/tmp/bot_db/" >> /etc/sendbot/sendbot.conf

echo "E-Mail-Address of the sendbot:"
read bot_addr
echo "Password of the sendbot"
read passwd
echo "Default sender-address of the sendmailscript"
read default

echo "DELTACHAT_BOT_ADDR=$bot_addr" >> /etc/sendbot/sendbot.conf
echo "DELTACHAT_BOT_PASSWORD=$passwd" >> /etc/sendbot/sendbot.conf
echo "DEFAULT_FROM=$default" >> /etc/sendbot/sendbot.conf

cp scripts/sendbot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now sendbot.service
