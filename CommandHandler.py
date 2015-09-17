__author__ = 'mariusmetzger'

import sys


class CommandHandler():

    COMMANDS = {
        "chats": ("Enables, disables or lists all chats this bot is active in", "chats <add|remove|list> <chatname>"),
        "modules": ("Loads, unloads or lists external modules", "modules <add|remove|list> <filename>"),
        "roles": ("Sets or gets a user's role or lists all available roles", "roles <set|get|list> <username> <role>"),
        "exit": ("Safely stops the bot", "exit"),
        "help": ("Displays this help page", "help")
    }

    NL = "\r\n"

    skypebot = None

    def __init__(self, skypebot):
        self.skypebot = skypebot

    def on_command_input(self, input):
        args = input.split()

        if len(args) <= 0:
            return

        command = args[0]
        args = args[1:]

        func = None
        try:
            func = getattr(self, command)
        except:
            pass

        if func is not None:
            ret = func(args)
            if ret == None:
                return "Usage: {0}".format(self.COMMANDS[command][1])

            return ret

        module_exec = None
        module_name = None
        for module in self.skypebot.modules:
            if module["display_name"] == command:
                module_name = module["display_name"]
                module_exec = module["module"]
                break

        if module_exec is not None:
            func = None
            try:
                func = getattr(module_exec, "on_command")
            except:
                pass

            if func is None:
                return "Module {0} has no on_command function".format(module_name)

            return func(self.skypebot, args)

        return "Unknown command \"{0}\"".format(command)

    def chats(self, args):
        if len(args) <= 0:
            return

        if args[0] == "add" or args[0] == "remove":
            if(len(args) < 2):
                return

            chatname = args[1]

            success = self.skypebot.chatHandler.set_chat_enabled(chatname, args[0] == "add")

            if args[0] == "add":
                if success:
                    return "Chat {0} has been successfully enabled".format(chatname)
                else:
                    return "Chat {0} is already enabled".format(chatname)

            else:
                if success:
                    return "Chat {0} has been successfully disabled".format(chatname)
                else:
                    return "Chat {0} is already disabled".format(chatname)

        if args[0] == "list":
            chats = "Enabled chats:"
            for chat in self.skypebot.chatHandler.get_enabled_chats():
                chats += "{0}{1}".format(self.NL, chat)

            return chats

    def modules(self, args):
        if len(args) <= 0:
            return

        if args[0] == "add" or args[0] == "remove":
            if(len(args) < 2):
                return

            module_name = args[1]

            result = self.skypebot.load_module(module_name)

            if args[0] == "add":
                if result is not None:
                    return "Module {0} was successfully loaded".format(result)
                else:
                    return "File {0} could not be found in /modules".format(module_name)

            else:
                if result:
                    return "Module {0} was successfully unloaded".format(module_name)
                else:
                    return "Module {0} could not be unloaded".format(module_name)

        if args[0] == "list":
            if len(self.skypebot.modules) > 0:
                modules = "Loaded modules:"
                for module in self.skypebot.modules:
                    modules += "{0}{1} - {2}".format(self.NL, module["module_name"], module["display_name"])

                return modules

            return "No external modules loaded"

    def roles(self, args):
        if len(args) <= 0:
            return

        if args[0] == "get":
            if len(args) < 2:
                return

            username = args[1]

            role_name = self.skypebot.permissionHandler.get_role_name(
                self.skypebot.permissionHandler.get_user_role(username))

            return "User {0} has role {1}".format(username, role_name)

        if args[0] == "set":
            if len(args) < 3:
                return

            username = args[1]
            role_name = args[2]

            success = self.skypebot.permissionHandler.set_user_role(username, role_name)

            if success:
                role_name = self.skypebot.permissionHandler.get_role_name(
                    self.skypebot.permissionHandler.get_user_role(username))

                return "User {0} now has the role {1}".format(username, role_name)
            else:
                return "Role {0} does not exist{1}" \
                       "Type \"roles list\" to list all available roles".format(role_name, self.NL)

        if args[0] == "list":
            roles = "Available roles:"
            for role_id, role_name in self.skypebot.permissionHandler.ROLES.iteritems():
                roles += "{0}{1}: {2}".format(self.NL, role_id, role_name)

            return roles

    def exit(self, args):
        self.skypebot.exit()
        return "Stopping the bot..."

    def help(self, args):
        help_page = "Available commands:"
        for command, details in self.COMMANDS.iteritems():
            help_page += "{0}{1}: {2}{3}\tUsage: {4}".format(self.NL, command, details[0], self.NL, details[1])

        return help_page