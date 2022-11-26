import os

blacklist = ['all_events.py']
package = 'events'

bot_events = []

# import bot events from all files in the `package` folder
for file in os.scandir(f'./{package}'):
    name, ext = os.path.splitext(file.name)
    if file.is_file() and ext == '.py' and file.name not in blacklist:
        module = f'{package}.{name}'
        bot_events += getattr(__import__(module), name).exported_events
