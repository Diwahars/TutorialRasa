from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import warnings

from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig
from rasa_core.run import serve_application


def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu/default/current")
    action_endpoint = EndpointConfig(url="http://localhost:5056/webhook")
    agent = Agent.load("models/dialogue", interpreter=interpreter, action_endpoint=action_endpoint)

    if serve_forever:
        serve_application(agent, channel='cmdline')
    return agent


if __name__ == '__main__':
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
            description='starts the bot')

    parser.add_argument(
            'task',
            choices=["train-nlu", "train-dialogue", "run"],
            help="what the bot should do?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "run":
        run()