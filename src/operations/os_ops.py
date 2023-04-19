import platform


def is_mac():
    return platform.system().lower() == 'darwin'
