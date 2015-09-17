__author__ = 'mariusmetzger'

class ChatHandler():

    KEY = "skypy:chats"

    redis = None

    def __init__(self, redis):
        self.redis = redis

    def set_chat_enabled(self, chatname, enabled):
        if enabled:
            if self.is_chat_enabled(chatname):
                return False

            self.redis.lpush(self.KEY, chatname)
        else:
            if not self.is_chat_enabled(chatname):
                return False

            self.redis.lrem(self.KEY, 0, chatname)

        return True

    def is_chat_enabled(self, chatname):
        return chatname in self.get_enabled_chats()

    def get_enabled_chats(self):
        return self.redis.lrange(self.KEY, 0, -1)

