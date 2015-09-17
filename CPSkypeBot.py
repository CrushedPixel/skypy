__author__ = 'mariusmetzger'

import imp, os
import traceback
import LenientConfigParser
import ChatHandler
import PermissionHandler
import CommandHandler
import Skype4Py
import redis

class CPSkypeBot:

    modules = []

    terminate = False
    configParser = None
    skype = None
    redis = None
    commandHandler = None
    chatHandler = None
    permissionHandler = None

    def load_module(self, filename):
        try:
            curdir = os.path.dirname(os.path.abspath(__file__))
            module_dir = os.path.join(curdir, "modules")
            module_file = os.path.join(module_dir, filename)
            module_file_name = os.path.splitext(filename)[0]

            module = imp.load_source(module_file_name, module_file)

            module_display_name = getattr(module, "moduleName")
            if module_display_name == None:
                module_display_name = module_file_name

            self.modules.append({"module_name": module_file_name,
                                 "display_name": module_display_name,
                                 "module": module})

            return module_display_name

        except:
            return

    def unload_module(self, module_name):
        for module in self.modules:
            if module["module_name"] == module_name or module["display_name" == module_name]:
                del(module)
                return True

        return False

    def _on_message_status_change(self, message, status):
        if self.chatHandler.is_chat_enabled(message.Chat.Name) \
                and self.permissionHandler.get_user_role(message.Sender.Handle) is not 2: #user is not muted
            if status == Skype4Py.cmsReceived or status == Skype4Py.cmsSent:
                for module in self.modules:
                    status_change_listener = None
                    try:
                        status_change_listener = getattr(module["module"], "on_message_status_change")
                    except:
                        pass

                    if status_change_listener is not None:
                        status_change_listener(self, message, status)

    def _run_command(self, input):
        return self.commandHandler.on_command_input(input)

    #public methods that are allowed to be called by module extensions
    def exit(self):
        self.configParser.write(open('skypy.cfg', 'w+'))
        self.terminate = True

    def send_group_chat_message(self, chat_name, message):
        chat = self.skype.Chat(chat_name)
        chat.SendMessage(message)

    def run(self):
        while not self.terminate:
            input = raw_input()
            print self._run_command(input)

    def __init__(self):
        print "Loading configuration file..."

        curdir = os.path.dirname(os.path.abspath(__file__))
        cfg = os.path.join(curdir, 'skypy.cfg')

        if not os.path.isfile(cfg):
            print "No configuration file found. Creating skypy.cfg..."
            cfg_handle = open(cfg, 'w+')

        else:
            cfg_handle = open(cfg)

        self.configParser = LenientConfigParser.LenientConfigParser()
        self.configParser.readfp(cfg_handle)

        #connecting to running Skype client
        print "Connecting to Skype client..."
        self.skype = Skype4Py.Skype()
        self.skype.Attach()

        self.skype.OnMessageStatus = self._on_message_status_change

        #connecting to Redis server
        redis_host = self.configParser.get("redis", "host")
        redis_port = self.configParser.get("redis", "port")
        redis_db = self.configParser.get("redis", "db")
        redis_pw = self.configParser.get("redis", "password")

        print "Connecting to Redis server..."
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_pw)
        try:
            self.redis.client_list()
            print "Connection to Redis server established"
        except:
            print(traceback.format_exc())
            print "Could not connect to Redis server. Please enter correct connection details in skypy.cfg"
            self.exit()

        self.commandHandler = CommandHandler.CommandHandler(self)
        self.chatHandler = ChatHandler.ChatHandler(self.redis)
        self.permissionHandler = PermissionHandler.PermissionHandler(self.redis)