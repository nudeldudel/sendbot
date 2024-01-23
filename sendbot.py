import deltachat
from deltachat import account_hookimpl, run_cmdline
from deltachat_rpc_client import events, run_bot_cli
import os

import asyncio
import logging

import json

from aiosmtpd.controller import Controller

host = os.getenv("DELTACHAT_HOST", default="")
port = os.getenv("DELTACHAT_PORT", default="25")
db_path = os.getenv("DELTACHAT_DB_PATH", default="/tmp/bot_db/")
ac = deltachat.Account(db_path)

addr = os.getenv("DELTACHAT_BOT_ADDR")
password = os.getenv("DELTACHAT_BOT_PASSWORD")

hooks = events.HookCollection()

class EchoPlugin:
    @account_hookimpl
    def ac_incoming_message(self, message):
        print("process_incoming message", message)
        if message.text.strip() == "/quit":
            message.account.shutdown()
        else:
            # unconditionally accept the chat
            message.create_chat()
            addr = message.get_sender_contact().addr
            if message.is_system_message():
                message.chat.send_text(f"System message from {addr}:\n{message}")
            else:
                text = message.text
                message.chat.send_text(f"__Please do not reply to this address!__\nOriginal: {addr}:\n{text}")

    @account_hookimpl
    def ac_message_delivered(self, message):
        print("ac_message_delivered", message)

    @hooks.on(events.NewMessage)
    def echo(event):
        snapshot = event.message_snapshot
        snapshot.chat.send_text(snapshot.text)

ac.run_account(addr=addr, password=password, account_plugins=[EchoPlugin()])

class ExampleHandler():
     async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
         ergebnis = ac.create_contact(address) # neu machen oder schon da
         global cid
         cid = ergebnis.id
         if not cid:
             return '550 not relaying to that reciever'
         envelope.rcpt_tos.append(address)
         return '250 OK'

     async def handle_DATA(self, server, session, envelope):
         absender = envelope.mail_from
         contact = deltachat.Contact(ac, cid)
         chatID = contact.create_chat()
         chat = deltachat.Chat(ac, chatID.id)
         #print('Message for %s' % envelope.rcpt_tos)
         #print('Message data:\n') # create_chat
         for ln in envelope.content.decode('utf8', errors='replace').splitlines():
             message =  ln.strip()
         msg = deltachat.message.Message.new_empty(ac, "text")
         msg.set_text(message)
         msg.is_bot()
         #msg.force_plaintext() # maybe it doesn't work with some scripts
         msg.set_override_sender_name(absender)
         ergebnis = chat.send_msg(msg)
         print (ergebnis) # send_message
         print('End of message')
         return '250 Message accepted for delivery'

async def amain(loop):
    cont = Controller(ExampleHandler(), hostname=host, port=port)
    cont.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.create_task(amain(loop=loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
