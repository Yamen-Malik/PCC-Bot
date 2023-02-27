<h1 align="center"> PCC Discord Bot </h1>

<p align="center">
    <a href="https://www.gnu.org/licenses/gpl-3.0">
        <img alt="GNU GPL v3.0" src="https://img.shields.io/badge/License-GPLv3-blue.svg">
    </a>
    <a href="https://www.python.org/downloads/release/python-3100/">
        <img alt="Python v3.10" src="https://img.shields.io/badge/Python-3.10-brightgreen?logo=python&logoColor=white">
    </a>
    <a href="https://github.com/Rapptz/discord.py/">
        <img alt="discord.py" src="https://img.shields.io/badge/discord-py-blue.svg?logo=discord&logoColor=white">
    </a>
    <a href="https://support.discord.com/hc/en-us/articles/1500000368501-Slash-Commands-FAQ">
        <img alt="supports slash commands" src="https://img.shields.io/badge/Supports-Slash%20Commands-success?logo=discord&logoColor=white&color=blue">
    </a>
    <br>
    <a href="https://github.com/psf/black">
        <img alt="black code style" src="https://img.shields.io/badge/code%20style-black-black">
    </a>
    <a href="https://github.com/Yamen-Malik/PCC-Bot/actions">
        <img alt="github actions" src="https://img.shields.io/github/actions/workflow/status/Yamen-Malik/PCC-Bot/linting.yml?event=push&label=tests">
    </a>
</p>

<br>

<p align="center">
    <a href="#About">About</a>
    •
    <a href="#installation-and-development-setup">Installation</a>
    •
    <a href="#contributing">Contributing</a>
</p>



## About

Open-source discord bot with slash commands support, mainly developed to automate and manage a discord server for a university student club.

The project is designed to be self-documented and easily customizable.

## Installation And Development Setup

### Requirements
1. **Python 3** - Follow instructions to install the latest version of python for your platform in the [python docs][install-python3].
2. **PIP Dependencies** - install dependencies by running the following command in the project directory:
   ```bash
   $ pip install -r requirements.txt
   ```
   This will install all of the required packages within the requirements.txt file.

### Authorization Setup

Create an environment variable called `BOT_TOKEN` and assign it's value to your bot secret token.

### Database Setup

The bot is hosted on [replit][replit-url] and therefore is using replit's free [key-value database][database].

A quick and easy workaround for local testing is to create a file called `replit.py` and adding an empty dictionary variable called `db`.

The file will look like this:
```py
db = {}
```
> Using this setup will cause the data to be cleared each time you restart the bot while testing locally.

Alternatively, if you're building your own bot and you're not going to use [replit][replit-url], you may want to consider [choosing another database][choose_database]. 

### Running The Bot

To run the bot you need to run `main.py` file by executing the following command:

```bash
$ python3 main.py
```


## Contributing

Please refer to the [contributing](CONTRIBUTING.md) guide to learn more about how to contribute to the project.


[gplv3-shield]: https://img.shields.io/badge/License-GPLv3-blue.svg
[gplv3-license]: https://www.gnu.org/licenses/gpl-3.0
[python3.10-shield]: https://img.shields.io/badge/Python-3.10-brightgreen?logo=python&logoColor=white
[python3.10]: https://www.python.org/downloads/release/python-3100/
[discord-py-shield]: https://img.shields.io/badge/discord-py-blue.svg
[discord.py]: https://github.com/Rapptz/discord.py/
[slash-commands-shield]: https://img.shields.io/badge/Supports-Slash%20Commands-success?logo=discord&logoColor=white
[slash-commands]: https://support.discord.com/hc/en-us/articles/1500000368501-Slash-Commands-FAQ
[replit-url]: https://replit.com
[install-python3]: https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python
[database]: https://docs.replit.com/hosting/databases/replit-database
[choose_database]: https://medium.com/wix-engineering/how-to-choose-the-right-database-for-your-service-97b1670c5632