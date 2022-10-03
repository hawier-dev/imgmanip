def create_time_str(str_to_create, seconds):
    str_to_create = str_to_create
    minutes, seconds = divmod(round(seconds, 2), 60)
    seconds = round(seconds, 2)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        if hours == 1:
            str_to_create += f' {hours} hour'
        else:
            str_to_create += f' {hours} hours'

    if minutes > 0:
        if minutes == 1:
            str_to_create += f' {minutes} minute'
        else:
            str_to_create += f' {minutes} minutes'

    if minutes == 1:
        str_to_create += f' {seconds} second'
    else:
        str_to_create += f' {seconds} seconds'

    return str_to_create
