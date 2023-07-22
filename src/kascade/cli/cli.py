import argparse
import asyncio
import importlib.util
import inspect
import logging
import pathlib
import sys

from types import ModuleType
from typing import Optional

from kascade import Table, Kascade

log: logging.Logger = logging.getLogger(__name__)


def get_action() -> Optional[str]:
    if len(sys.argv) < 1:
        return
    if sys.argv[1] not in ['get', 'apply', 'delete']:
        return
    return sys.argv[1]


def action_to_table_help(action: Optional[str] = None) -> str:
    if action is None:
        return 'You can "get", "apply" changes or "delete" your tables'
    elif action == 'get':
        return 'Get table information'
    elif action == 'apply':
        return 'Apply changes to your table structure'
    elif action == 'delete':
        return 'Delete tables from your database'
    else:
        log.error(f'Invalid action: {action}')
        sys.exit(1)


def is_python_file(path: str) -> str:
    path = pathlib.Path(path)
    if not path.exists():
        raise argparse.ArgumentTypeError(
            f'{path} does not exist.\n\t You should create a file containing the tables definition.'
        )
    if not path.is_file():
        raise argparse.ArgumentTypeError(
            f'{path} is not a file.\n\t You should create a file containing the tables definition.'
        )
    if path.suffix != '.py':
        raise argparse.ArgumentTypeError(
            f'{path} is not a python file.\n\t You should create a file containing the tables definition.'
        )
    return path


def import_file(path: pathlib.Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location('tables', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_diff(tables_path: pathlib.Path):
    pass


async def get_table(tables_path: pathlib.Path):
    tables = import_file(tables_path)
    declared_tables = inspect.getmembers(tables, inspect.isclass)

    print(f'{" #" * 5}  KASCADE CONFIGURATION {"# " * 5}\n')
    for _, table in declared_tables:
        if not issubclass(table, Table) or table == Table:
            continue
        print(f'Table: {table.get_table_name()}')
        for key, value in table.__fields__.items():
            print(
                f'\t{key}: {str(value).replace("annotation=", "")}'
            )
        print()
    
    print(f'{" #" * 5} DATABASE CONFIGURATION {"# " * 5}')
    async with Kascade() as db:
        await db.get_tables()


def apply_table(tables_path: pathlib.Path):
    tables = import_file(tables_path)
    
    declared_tables = inspect.getmembers(tables, inspect.isclass)

    for _, table in declared_tables:
        if not issubclass(table, Table) or table == Table:
            continue
        print(f'Table: {table.get_table_name()}')
        for key, value in table.__fields__.items():
            print(
                f'\t{key}: {str(value).replace("annotation=", "")}'
            )
        print()


def main():
    parser = argparse.ArgumentParser(
        prog='Kascade',
        description='Python ORM for SQL Databases based on Pydantic',
        epilog=f'For more information, visit https://github.com/fernaper/kascade-orm'
    )

    parser.add_argument(
        'action',
        type=str,
        help='Action to be performed',
        choices=['get', 'apply', 'delete']
    )

    parser.add_argument(
        'object',
        type=str,
        help=action_to_table_help(get_action()),
        choices=['table',], # In the future we may add more objects
        default='table',
    )

    parser.add_argument(
        '--tables-path',
        type=is_python_file,
        help='Path to the python file containing the tables definition',
        default='tables.py'
    )

    # TODO: Maybe accept a settings kwarg to override the default settings

    args = parser.parse_args()

    if args.object == 'table':
        if args.action == 'get':
            asyncio.run(get_table(args.tables_path))
        elif args.action == 'apply':
            apply_table(args.tables_path)
        elif args.action == 'delete':
            pass


if __name__ == '__main__':
    main()
