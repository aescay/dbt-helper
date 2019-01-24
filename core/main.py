import argparse
import sys

import core.bootstrap as bootstrap_task
import core.compare as compare_task

from dbt.config import RuntimeConfig, PROFILES_DIR
from dbt.compilation import Compiler
import dbt.adapters.factory


def parse_args(args):

    p = argparse.ArgumentParser(
        prog="mkdbt: additional tools for wokring with DBT",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Additional CLI tools for faster DBT development and database management",
        epilog="Select one of these sub-commands and you can find more help from there.",
    )

    base_subparser = argparse.ArgumentParser(add_help=False)
    base_subparser.add_argument(
        "--profiles-dir",
        default=PROFILES_DIR,
        type=str,
        help="""
        Which directory to look in for the profiles.yml file. Default = {}
        """.format(
            PROFILES_DIR
        ),
    )
    base_subparser.add_argument(
        "--profile",
        required=False,
        type=str,
        help="""
        Which profile to load. Overrides setting in dbt_project.yml.
        """,
    )
    base_subparser.add_argument(
        "--target",
        default=None,
        type=str,
        help="Which target to load for the given profile",
    )

    subs = p.add_subparsers(title="Available sub-commands", dest="command")

    compare_sub = subs.add_parser(
        "compare",
        parents=[base_subparser],
        help="Compare your dbt project specifications with what's in your database.",
    )
    compare_sub.set_defaults(cls=compare_task.CompareTask, which="compare")

    bootstrap_sub = subs.add_parser(
        "bootstrap",
        parents=[base_subparser],
        help="Bootstrap schema.yml files from database catalog",
    )
    bootstrap_sub.set_defaults(cls=bootstrap_task.BootstrapTask, which="bootsrap")

    bootstrap_sub.add_argument(
        "--schemas",
        required=True,
        nargs="+",
        help="""
        Required. Specify the schemas to inspect when bootstrapping
        schema.yml files.
        """,
    )
    bootstrap_sub.add_argument(
        "--single-file",
        action="store_true",
        dest="single_file",
        help="Store all of the schema information in a single schema.yml file",
    )
    bootstrap_sub.add_argument(
        "--print-only",
        action="store_true",
        dest="print_only",
        help="Print generated yml to console. Don't attempt to create schema.yml files.",
    )

    if len(args) == 0:
        p.print_help()
        sys.exit(1)
        return

    parsed = p.parse_args(args)
    return parsed


def handle(args):
    parsed = parse_args(args)
    results = None

    if parsed.command == "bootstrap":
        task = bootstrap_task.BootstrapTask(parsed)
        results = task.run()

    if parsed.command == "compare":
        task = compare_task.CompareTask(parsed)
        results = task.run()

    return results


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    handle(args)


if __name__ == "__main__":
    main()
