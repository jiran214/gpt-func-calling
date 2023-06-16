from typing import List

Limit = 1500


def filter_html(text_list: List[str]):
    new_text_list = []
    current_len = 0
    is_newline_character_last = False
    for text in text_list:
        if text == '\n':
            if is_newline_character_last is False:
                new_text_list.append(' ')
                current_len += len(text)
                is_newline_character_last = True
        else:
            is_newline_character_last = False
            new_text_list.append(text)
            current_len += len(text)

        if current_len > Limit:
            break
    return ''.join(new_text_list)