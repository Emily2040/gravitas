"""Serve files a user uploaded earlier."""
import os

UPLOAD_ROOT = "/srv/uploads"


def read_user_file(user_id, name):
    """Return the contents of one of the user's uploaded files."""
    path = os.path.join(UPLOAD_ROOT, str(user_id), name)
    with open(path, "rb") as fh:
        return fh.read()
