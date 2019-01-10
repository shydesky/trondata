class Colors:
    """ 用来彩色输出方便调试或者输出一些重要信息
    Usage:
        print(
            Colors.FAIL+ "Warning: No active frommets remain. Continue?" +
            Colors.ENDC
        )
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class _Missing(object):

    def __bool__(self):
        return False

    __nonzero__ = __bool__  # PY2 compat

    def __repr__(self):
        return '<form.missing>'

missing_singleton = _Missing()