#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
<<<<<<< HEAD
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qgeoidcolweb.settings")
=======
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project3.settings')
>>>>>>> origin/web50/projects/2020/x/mail
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


<<<<<<< HEAD
if __name__ == "__main__":
=======
if __name__ == '__main__':
>>>>>>> origin/web50/projects/2020/x/mail
    main()
