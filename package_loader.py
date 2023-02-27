import os
from logging import getLogger

from discord.ext.commands import Bot


PACKAGES = ["commands", "events"]


async def load_package(package: str, bot: Bot):
    """Loads a package by calling setup function in all its modules

    Args:
        package (str): package name
        bot (Bot): bot object to pass to setup functions
    """

    # get the directory of this script
    directory = os.path.dirname(os.path.realpath(__file__))

    package_directory = f"{directory}/{package}"

    # load all files in the package
    for file in os.scandir(package_directory):
        name, ext = os.path.splitext(file.name)

        # load only python files
        if file.is_file() and ext == ".py":
            try:
                # import and call setup function
                module = f"{package}.{name}"
                module = getattr(__import__(module), name)

                await module.setup(bot)
            except AttributeError as error:
                getLogger(__name__).error(error)


async def load_cogs(bot: Bot):
    """Loads all Cogs and groups

    Args:
        bot (Bot): bot object to load cogs into
    """

    for package in PACKAGES:
        await load_package(package, bot)
