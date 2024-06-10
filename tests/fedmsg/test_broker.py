
import time
from webhook_to_fedora_messaging.fedmsg.broker import FedMsgBroker
from fedora_messaging import api
import threading

msg=None
def test_broker():
    """
        Publishes a message and then consumes it with FedMsgBroker to validate if the messages are the same and valid.
    """
    
    broker = FedMsgBroker(logging=False)
    message_sent = api.Message(topic="hello", body={"Hello": "world!"})
    th = threading.Thread(target=broker.consume, args=[get_message])
    th.start()
    time.sleep(5)
    broker.publish(message_sent)
    while msg is None:
        time.sleep(0.5)
    th.join()
    assert message_sent == msg
    
    
# Used as callback to consume.
def get_message(message):
    global msg
    msg = message
    exit()