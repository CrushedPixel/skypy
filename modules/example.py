__author__ = 'mariusmetzger'

# the module's display name. If not defined, the file's base name is used
moduleName = "example"

# whenever a message is sent to one of the enabled chats by a user who is not blacklisted, this method is called
def on_message_status_change(skypebot, message, status):
    pass

# whenever a command prefixed with this module's display name is executed, this method is called
# example:
def on_command(skypebot, args):
    return "Command delivered!"