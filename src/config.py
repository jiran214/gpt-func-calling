import configparser
import os.path

root_path = os.path.abspath(os.path.dirname(__file__))
_file_path = os.path.join(root_path, 'config.ini')

_config = configparser.RawConfigParser()
_config.read(_file_path)

api_key = _config.get('openai', 'api_key')
proxy = _config.get('openai', 'proxy')
cookie_settings = dict(_config.items('tool_cookie'))
google_settings = dict(_config.items('google'))