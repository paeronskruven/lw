import argparse
import sqlite3
import sys
import os
import configparser
import importlib
import itertools
import threading
import logging

from . import sources
from .data import calls
from .notifications import notify


config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.lw/lw.conf'))


def watch(args):
    key = args.keyword.lower()
    try:
        calls.add_keyword(key)
        print('Now watching {0}'.format(key))
    except sqlite3.IntegrityError:
        print('{0} is already being watched'.format(key))


def unwatch(args):
    key = args.keyword.lower()
    if calls.remove_keyword(key):
        print('Unwatched {0}'.format(key))
    else:
        print('{0} was not found on watch list'.format(key))


def list_(args):
    keywords = calls.list_keywords()
    print('Currently watching:')
    for key in keywords:
        print(key[0])


def progress(evt_stop):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while not evt_stop.wait(0.2):
        print('\b' + next(spinner), end='')
        sys.stdout.flush()
    print('\b', end='')
    sys.stdout.flush()


def run(args):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(os.path.expanduser('~/.lw/lw.log'))
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    evt_stop = threading.Event()
    t = threading.Thread(target=progress, args=(evt_stop,))
    t.start()

    for source in config.items('sources'):
        key, mod = source
        imod = importlib.import_module(mod)
        logger.info('Loading {0}'.format(imod))

    watch_results = {}
    for key in calls.list_keywords():
        logger.info('Query -> {0}'.format(key[0]))
        watch_results[key[0]] = sources.query(key[0])

    new_items = {}
    for key, item in watch_results.items():
        tmp = []
        for gen in item:
            if gen:
                tmp.append(calls.add_items(gen))
        tmp = list(itertools.chain.from_iterable(tmp))
        if len(tmp):
            new_items[key] = tmp

    evt_stop.set()
    t.join()

    if len(new_items):
        notify(new_items)


def main():
    parser = argparse.ArgumentParser(description='ListingsWatch')
    subparsers = parser.add_subparsers(title='commands')
    subparsers.required = True
    subparsers.dest = 'command'

    pw = subparsers.add_parser('watch')
    pw.add_argument('keyword')
    pw.set_defaults(func=watch)

    pu = subparsers.add_parser('unwatch')
    pu.add_argument('keyword')
    pu.set_defaults(func=unwatch)

    pl = subparsers.add_parser('list')
    pl.set_defaults(func=list_)

    pr = subparsers.add_parser('run')
    pr.set_defaults(func=run)

    args = parser.parse_args(sys.argv[1:])
    args.func(args)

if __name__ == '__main__':
    main()
