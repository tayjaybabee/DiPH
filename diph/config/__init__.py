from logging import getLogger
from pypattyrn.creational.singleton import Singleton

from inspy_logger import InspyLogger, LEVELS as LOG_LEVELS

import os
from pathlib import Path
from os import path

__VERSION__ = '1.0a1'

DEFAULT_APP_PATH = str(Path("~/Inspyre-Softworks/DiPH").expanduser())

CONF_DIR = DEFAULT_APP_PATH + '/config'
DEFAULT_DATA_PATH = DEFAULT_APP_PATH + '/data'

m_log_name = 'DiPHConfig'
root_log_device = InspyLogger(m_log_name, 'debug')
m_log = root_log_device.start()
m_debug = m_log.debug

m_debug(m_log_name + ' started!')

ENV_PATH = str(Path('~/.config/Inspyre-Softworks/DiPH').expanduser())

ENV_FILE = ENV_PATH + '/.env'

class EnvHandler(object):
    
    def create_new(self):
        from configparse import ConfigParse
        os.makedirs(ENV_PATH)

        env_obj = {
            'ENV': {
                'data-dir': 
            }
        }

    def load_existing(self):
        pass

    def remove_existing(self):
        pass
    
    def __init__(self, conf_path=None, env_path=None):
        if Path(ENV_PATH).exists():
            pass  # TODO: Figure out what -exactly- to do if `ENV_PATH` is present. Current idea:
                  #       - Open file, and (assuming it's not a malformed file) attempt to parse it to find the real configuration directory it points to
                  #       - Once the actual config file location is ascertained and tagged, confirm it exists, and it itself not in a malformed state
                  #       - ??
        else:
            self.conf_path = create_new()


class DiPHConfig(object, metaclass=Singleton):

    def __init__(self):``
        """

        Instantiate a new instance of a DiPHConfig object for the main DiPH program.

        """
        self.VERSION = __VERSION__
        """ The current version of the program """

        self.args = self.parse_arguments()
        self.runtime = {

            'args':  self.args,

        }
        self.conf_parser = None
        self.debug = m_debug
        self.log_device = root_log_device

        self.default_conf = self.default_config()

    def default_config(self):
        from configparser import ConfigParser
        """
        Will return a fully-formed default configuration dictionary to be read into a ConfigParser later

        Returns:
            dict: Dictionary object to be read into a ConfigParser later, complete with sections, etc.
        """

        _ = {
            'API.SETTINGS': {

                'api-key': '',

            },

            'APP.SETTINGS': {

                'app-data-dir': DEFAULT_DATA_PATH,
                'plugins-dir': DEFAULT_APP_PATH + '/plugins',

            },

            'BOT.SETTINGS': {

                'name': 'diphy',
                'cmd-prefix': '$',
                'attr-prefix': '.'


            },
        }

        parser = ConfigParser()
        parser.read_dict(_)

        self.runtime['config'] = parser
        print(dir(parser))

        return parser

    def create_new(self, app_dir, plugins_dir):
        """
        Create a new configuration object, and prepare the filesystem for runtime. `app_dir` and `plugins_dir` will be created if they don't already exist

        Args:
            app_dir (str): A string representing the path of the directory that you'd like this application's data to be stored in
            plugins_dir (str): A string representing the path of the directory that you'd like this application to look for plugin directories in
        """
        app_settings = self.default_config()['APP.SETTINGS']
        os.makedirs(app_settings['app-data-dir'])
        os.makedirs(app_settings['plugins-dir'])
        env = EnvHandler().start

    def parse_config(self):
        from configparser import ConfigParser

        pass

    def parse_arguments(self):
        """
        Define and then parse command-line arguments, then return the parsed data to the caller.

        Returns:
            ArgumentParser: A parsed `ArgumentParser` object.
        """
        from argparse import ArgumentParser

        a_parser = ArgumentParser(
            description='Discord Python Helper bot, config utility')

        a_parser.add_argument('-l', '--log-level',
                              nargs='?',
                              action='store',
                              choices=LOG_LEVELS,
                              default='info')

        a_parser.add_argument('-c', '--config-file',
                              type=str,
                              action='store',
                              default=CONF_DIR + '/diph.conf',
                              help="The location where either; you'd like to have a new configuration file written to; or you'd like to have a configuration state loaded from.")

        a_parser.add_argument('-k', '--api-key',
                              type=str,
                              action='store',
                              help="The API key for Discord. No API key, no run.")

        a_parser.add_argument('-n', '--bot-name',
                              type=str,
                              action='store',
                              help='The name that the bot will have on Discord')

        a_parser.add_argument('--prefix',
                              type=str,
                              action='store',
                              help="The prefix that you wish to have present at the beginning of every command passed to the bot. Having a prefix helps differentiate regular conversation and a direct request of the bot.")

        a_parser.add_argument('-V', '--version',
                              action='version',
                              version=self.VERSION)

        sub_parsers = a_parser.add_subparsers(title='subcommands',
                                              help='Some commands to assist with configuration.',
                                              dest='subcommands')

        cleanup_cmd = sub_parsers.add_parser(
            'cleanup', help='Remove any previous configuration files ')

        wizard_cmd = sub_parsers.add_parser(
            'wizard', help='The DiPH Configuration Wizard will walk you through every necessary step to get your bot up and running.')
        wizard_cmd.add_argument('--only-api-key',
                                help='Only ask for the Discord API key',
                                action='store',
                                default=None,)

        modify_cmd = sub_parsers.add_parser(
            'mod-conf', help='Modify an existing config file.')

        return a_parser.parse_args()