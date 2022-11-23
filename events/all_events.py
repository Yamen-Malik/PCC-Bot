# from events.on_ready import on_ready
# from events.on_member_join import on_member_join


import os

blacklist = ['all_events.py']
package = 'events'

bot_events = []

for file in os.scandir(f'./{package}'):
    name, ext = os.path.splitext(file.name)
    if not (file.is_file() and ext == '.py' and file.name not in blacklist):
        continue
    module = f'{package}.{name}'
    bot_events += getattr(__import__(module), name).exported_events
