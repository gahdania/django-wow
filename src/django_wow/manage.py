#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config

def main():
    """Run administrative tasks."""
    project_env = os.environ.get('PROJECT_ENV')

    if not project_env:
        project_env = config('PROJECT_ENV', default='local')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'django_wow.settings.{project_env}')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
