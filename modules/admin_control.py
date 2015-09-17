__author__ = 'mariusmetzger'

moduleName = "adminControl"

ADMIN_CONTROL_PREFIX = "!exec "

# allows administrators to execute commands on the skype bot without having access to the command line
# by prefixing their message with "!exec"
def on_message_status_change(skypebot, message, status):
    msg = message.Body
    if msg.startswith(ADMIN_CONTROL_PREFIX):
        if skypebot.permissionHandler.get_user_role(message.Sender.Handle) == 1: #if user is admin
            skypebot.send_group_chat_message(message.Chat.Name, skypebot._run_command(msg[len(ADMIN_CONTROL_PREFIX):]))
        else:
            skypebot.send_group_chat_message(message.Chat.Name, "You do not have permission to execute commands")