__author__ = 'mariusmetzger'

class PermissionHandler():

    ROLES = {
        0: "USER",
        1: "ADMIN",
        2: "MUTED"
    }

    COLON = ":"

    KEY = "skypy:{0}:role"

    redis = None

    def __init__(self, redis):
        self.redis = redis

    def set_user_role(self, username, role):
        role_id = None
        if role in self.ROLES.keys():
            role_id = role

        if role_id is None:
            id = self.role_by_name(role)
            if id is not None:
                role_id = id

        if role_id is None:
            return False

        self.redis.set(self.KEY.format(username), role_id)
        return True

    def get_user_role(self, username):
        role = self.redis.get(self.KEY.format(username))
        if role is None:
            return 0

        return int(role)

    def get_role_name(self, role):
        for role_id, role_name in self.ROLES.iteritems():
            if role_id == int(role):
                return role_name

        return None

    def role_by_name(self, name):
        for role_id, role_name in self.ROLES.iteritems():
            if role_name.upper() == name.upper():
                return role_id

        return None

