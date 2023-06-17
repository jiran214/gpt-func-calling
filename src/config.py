import configparser
import os.path

root_path = os.path.abspath(os.path.dirname(__file__))
_file_path = os.path.join(root_path, 'config.ini')

_config = configparser.RawConfigParser()
_config.read(_file_path)

api_key = _config.get('openai', 'api_key')
proxy = _config.get('openai', 'proxy')
proxies = {
    'http': f'http://{proxy}/',
    'https': f'http://{proxy}/'
}
google_settings = dict(_config.items('google'))
window_size = _config.getint('session', 'window_size')
tool_output_limit = _config.getint('tool', 'output_limit')