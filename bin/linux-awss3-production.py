#!/usr/bin/env python
# coding: utf-8

#
# Wire
# Copyright (C) 2018 Wire Swiss GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#

import boto3
import json
import os

BUCKET = os.environ.get('BUCKET')
VERSION = os.environ.get('WRAPPER_BUILD').split('#')[1]

bin_root = os.path.dirname(os.path.realpath(__file__))
build_root = os.path.join(bin_root, '..', 'wrap', 'dist')
S3_PATH = 'linux/'


def upload_file(source, destination):
    if not os.path.isfile(source):
        print '{} not found'.format(source)
        return

    print 'Uploading {SOURCE} to {DESTINATION}'.format(SOURCE=os.path.basename(source), DESTINATION=destination),
    s3 = boto3.resource('s3')

    data = open(source, 'rb')
    s3.Bucket(name=BUCKET).put_object(Key=destination, Body=data, ACL='public-read')
    print '- OK'


if __name__ == '__main__':
    files = [
        'sha256sum.txt.asc',
        'wire-{VERSION}-i386.AppImage'.format(VERSION),
        'wire-{VERSION}-x86_64.AppImage'.format(VERSION),
        'debian/pool/main/wire{VERSION}_amd64.deb'.format(VERSION),
        'debian/pool/main/wire_{VERSION}_i386.deb'.format(VERSION),
        'debian/dists/stable/Contents-all',
        'debian/dists/stable/Contents-all.bz2',
        'debian/dists/stable/Contents-all.gz',
        'debian/dists/stable/Contents-amd64',
        'debian/dists/stable/Contents-amd64.bz2',
        'debian/dists/stable/Contents-amd64.gz',
        'debian/dists/stable/Contents-i386',
        'debian/dists/stable/Contents-i386.bz2',
        'debian/dists/stable/Contents-i386.gz',
        'debian/dists/stable/InRelease',
        'debian/dists/stable/Release',
        'debian/dists/stable/Release.gpg',
        'debian/dists/stable/main/binary-all/Packages',
        'debian/dists/stable/main/binary-all/Packages.bz2',
        'debian/dists/stable/main/binary-all/Packages.gz',
        'debian/dists/stable/main/binary-amd64/Packages',
        'debian/dists/stable/main/binary-amd64/Packages.bz2',
        'debian/dists/stable/main/binary-amd64/Packages.gz',
        'debian/dists/stable/main/binary-i386/Packages',
        'debian/dists/stable/main/binary-i386/Packages.bz2',
        'debian/dists/stable/main/binary-i386/Packages.gz',
    ]

    for filename in files:
        upload_file(os.path.join(build_root, filename), '{PATH}{FILENAME}'.format(PATH=S3_PATH, FILENAME=filename))