from fedora_messaging import api, config, message
from typing import Callable
from webhook_to_fedora_messaging.config import CONF_PATH


class FedMsgBroker:
    
    def __init__(self, logging: bool=True) -> None:
        if logging:
            config.conf.setup_logging()
    
    def publish(self, message: message.Message):
        api.publish(message)
    
    def consume(self, callback: Callable):
        api.consume(lambda message: callback(message))
        
        

    