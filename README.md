# skypy
skypy is an extensible Skype Bot written in Python. \
Write your own modules to add any functionality you wish.

### Getting started
To get started, you need the [Skype4Py](https://pypi.python.org/pypi/Skype4Py/) and [redis](https://pypi.python.org/pypi/redis) libraries, a running Skype client and well as a redis server.\
The redis server is required to store for which conversations the bot is enabled, and to save user permissions.

In the `skypy.cfg` file, edit the connection details for your redis server.

If it isn't running already, start the Skype client on your server. Of course, you need a desktop environment like GNOME.

You can now launch skypy. When starting it the first time, you have to accept the connection between skypy and your Skype client.

This was tested with Debian 8.2, GNOME and Skype for Linux Version 4.3.

### Available commands
The following commands are available by default:

`chats <add|remove|list> <chatname>`\
Enables, disables or lists all chats this bot is active in

`modules <add|remove|list> <filename>`\
Loads, unloads or lists external modules from the `modules` folder

`roles <set|get|list> <username> <role>`\
Sets or gets a user's role or lists all available roles

`exit`\
Safely stops the bot

`help`\
Displays a help page

Every module you add can have an `on_command` handler which is triggered when you prefix your console input with the module's display name. For more information, see [example.py](modules/example.py).

### Pre-installed modules
#### adminControl
As of now, there's only one functional module pre-installed in skypy: `admin_command.py`. You can enable it using `modules add admin_command.py`.\

Whenever a user with ADMIN role writes a message into a skype group that is prefixed with `!exec`, skypy is going to handle the message like a command entered in the console.

Example: Writing `!exec roles list` as an ADMIN makes the Skype Bot output all available roles in the Skype group.

### Adding own modules
Writing modules is simple: Just add a Python file to the `modules` folder. You can then load this module using `modules add filename.py`.\
See [example.py](modules/example.py) for an example module.

If you have written some nice modules you'd like to see in the default modules, simply create a pull request.

### License
skypy &copy; 2015 Marius Metzger\
skypy is licensed under the [Apache 2.0 License](http://apache.org/licenses/LICENSE-2.0).
