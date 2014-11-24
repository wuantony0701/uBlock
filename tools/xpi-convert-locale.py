#!/usr/bin/env python3

import os
import json
import sys
from shutil import rmtree as rmt
from collections import OrderedDict

if not sys.argv[1]:
	raise SystemExit('Build dir missing.')

osp = os.path
pj = osp.join


def rmtree(path):
    if osp.exists(path):
        rmt(path)


def mkdirs(path):
    try:
        os.makedirs(path)
    finally:
        return osp.exists(path)


build_dir = osp.abspath(sys.argv[1])
source_locale_dir = pj(build_dir, '_locales')
target_locale_dir = pj(build_dir, 'locale')

for alpha2 in os.listdir(source_locale_dir):
    locale_path = pj(source_locale_dir, alpha2, 'messages.json')
    with open(locale_path, encoding='utf-8') as f:
        string_data = json.load(f, object_pairs_hook=OrderedDict)

    alpha2 = alpha2.replace('_', '-')

    mkdirs(pj(target_locale_dir, alpha2))

    locale_path = pj(target_locale_dir, alpha2, 'messages.properties')
    with open(locale_path, 'wt', encoding='utf-8', newline='\n') as f:
        for string_name in string_data:
            f.write(string_name)
            f.write('=')
            f.write(string_data[string_name]['message'].replace('\n', r'\n'))
            f.write('\n')

rmtree(source_locale_dir)