from fedora_messaging import api, config, message
import os
import toml
from webhook_to_fedora_messaging.config import TEMPLATE, CONF_PATH





class FedMsgBroker:
    
    def __init__(self, connection_uri:str, key_file: str, cert_file: str, ca_cert: str) -> None:
        self.__config = self.__generate_config(connection_uri, key_file, cert_file, ca_cert)
        config.conf.setup_logging()
        os.environ['FEDORA_MESSAGING_CONF"'] = CONF_PATH
        self.__save_config()

        
            
    def __generate_config(self, connection_uri:str, key_file: str, cert_file: str, ca_cert: str) -> None:
        """
            Generating a config file according to needs.
            
            Args:
                connection_uri: rabbitmq host to connect
                key_file: path to key file
                cert_file: path to cert file
                ca_cert: path to ca cert file
    
        """
        conf = self.__get_template_config()
        conf['amqp_url'] = connection_uri if connection_uri != "" else conf['amqp_url']
        conf['keyfile'] = key_file
        conf['certfile'] = cert_file
        conf['ca_cert'] = ca_cert
        return conf
    
    def __save_config(self):
        with open(CONF_PATH, "w") as file:
            toml.dump(self.__config, file)
    
    
    

    def set_config(self, value: dict):
        """
            Takes a dictionary as a value and sets the options in the dictionary keys to the corresponding values in the dictionary.
            
            
        """
        
        for key, setting in value.items():
            self.__config[key] = setting
        self.__save_config()
        
            
    # Returns the default config.            
    def __get_template_config(self):
        return self.__get_config(TEMPLATE)
            
            
    def __get_config(self, path: str):
        with open(path, "r") as file:
            return toml.load(file)
    
    
    def publish(self, message: message.Message):
        api.publish(message)
        
    
    def consume(self):
        api.consume(lambda message: print(message))
        
        

    