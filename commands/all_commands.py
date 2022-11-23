import os

blacklist = ['all_commands.py']
package = 'commands'

bot_commands = []

for file in os.scandir(f'./{package}'):
    name, ext = os.path.splitext(file.name)
    if not (file.is_file() and ext == '.py' and file.name not in blacklist):
        continue
    module = f'{package}.{name}'
    bot_commands += getattr(__import__(module), name).exported_commands
