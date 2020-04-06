
_id_counter = 0


def next_id():
    global _id_counter
    _id_counter += 1
    return _id_counter


def next_tmp_name():
    return f"tmp{next_id()}"