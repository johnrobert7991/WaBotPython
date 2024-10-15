import logging
import os
import signal
import sys

from corcel import Corcel
from datetime import timedelta

from neonize.client import NewClient
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    event,
    ReceiptEv,
    CallOfferEv,
    QREv
)
from neonize.proto.Neonize_pb2 import JID
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    FutureProofMessage,
    InteractiveMessage,
    MessageContextInfo,
    DeviceListMetadata,
)
from neonize.types import MessageServerID
from neonize.utils import log
from neonize.utils.enum import ReceiptType
from neonize import Event


def interrupted(*_): 
    event.set()


log.setLevel(logging.CRITICAL)
signal.signal(signal.SIGINT, interrupted)

client = NewClient("db.sqlite3")
client_chat = Corcel()
client_chat.history = []

@client.event(ConnectedEv)
def on_connected(_: NewClient, __: ConnectedEv):
    log.info("⚡ Connected")


@client.event(ReceiptEv)
def on_receipt(_: NewClient, receipt: ReceiptEv):
    log.debug(receipt)


@client.event(CallOfferEv)
def on_call(_: NewClient, call: CallOfferEv):
    log.debug(call)


@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    handler(client, message)


def handler(client: NewClient, message: MessageEv):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    log.critical(f"Incoming Message: \n{message.Message}")
    # log.critical(message.Message)
    # log.critical("==============")
    # log.critical(message.Message)
    # log.critical("\n")
    
    if text.startswith("ping"): 
        client.reply_message("pong", message)

    elif text.startswith("/ask"): 
        prompt = text.lstrip("/ask").strip()
        if not prompt: 
            client.reply_message(
                (
                    "usage /ask <prompt>\n"
                    "example: /ask apa itu kucing?"
                ),
                message
            )
            return
        
        resp = client_chat.chat(prompt, history=client_chat.history)
        client.reply_message(resp, message)


@client.event(PairStatusEv)
def PairStatusMessage(_: NewClient, message: PairStatusEv):
    log.info(f"logged as {message.ID.User}")     

def main():
    code = client.PairPhone("6285155304081", show_push_notification=False)  # Jalankan client dalam loop selamanya

if __name__ == "__main__": 
    print("Hello")
    main()
    # print(code)
    

