class _SessionState(dict):
    pass

session_state = _SessionState()

# Basic UI placeholder functions

def radio(label, options):
    return options[0]

def file_uploader(*a, **k):
    return None

def text_area(*a, **k):
    return ""

def columns(n):
    class Dummy:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
    return [Dummy() for _ in range(n)]


def write(*a, **k):
    pass

def subheader(*a, **k):
    pass

def selectbox(*a, **k):
    return None

def button(*a, **k):
    return False

def checkbox(*a, **k):
    return False

def download_button(*a, **k):
    pass

def warning(*a, **k):
    pass

def error(*a, **k):
    pass

def success(*a, **k):
    pass

def info(*a, **k):
    pass

def code(*a, **k):
    pass

def text_input(*a, **k):
    return ""

def spinner(*a, **k):
    class Dummy:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
    return Dummy()


def tabs(labels):
    class Dummy:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
    return [Dummy() for _ in labels]

def header(*a, **k):
    pass

def divider():
    pass

def markdown(*a, **k):
    pass

def expander(*a, **k):
    class Dummy:
        def write(self, *a, **k):
            pass
    return Dummy()

def set_page_config(*a, **k):
    pass
