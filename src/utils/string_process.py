from typing import List

import config
from utils.utils import num_tokens_from_string

Limit = config.tool_output_limit


def filter_html(text_list: List[str], length_func=num_tokens_from_string):
    """去除多余换行，限制总长度在<Limit>"""
    new_text_list = []
    current_len = 0
    is_newline_character_last = False
    for text in text_list:
        if text in {'\n', '▪', '\xa0'} or text.startswith('\n['):
            if is_newline_character_last is False:
                new_text_list.append(' ')
                current_len += length_func(text)
                is_newline_character_last = True
        else:
            is_newline_character_last = False
            new_text_list.append(text)
            current_len += length_func(text)

        if current_len > Limit:
            new_text_list.pop()
            break
    return ''.join(new_text_list)

