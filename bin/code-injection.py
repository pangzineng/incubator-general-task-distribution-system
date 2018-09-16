# coding: utf-8

import argparse
import os
import re
import glob
from shutil import copyfile

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-p','--path', help='the python-flask-server folder', required=True)
parser.add_argument('-t','--temdir', help='the dir to the injected codes', required=True)
parser.add_argument('-o','--port', help='the port number to replace flask default 8080', default="8888")
args = parser.parse_args()

controller_template = open('{}/controller_template.py'.format(args.temdir),'r').read()

for controller in glob.glob('{}/swagger_server/controllers/*_controller.py'.format(args.path)):
    with open(controller, 'w') as f:
        f.write(controller_template.replace('${KEY}', controller.split('/')[-1].split('_')[0]))

encoder_custom = open('{}/encoder_custom_bson.py'.format(args.temdir), 'r').read()
with open('{}/swagger_server/encoder.py'.format(args.path), 'w') as f:
    f.write(encoder_custom)

with open('{}/requirements.txt'.format(args.path), 'a') as f:
    with open('{}/requirements.txt'.format(args.temdir)) as infile:
        f.write(infile.read())

copyfile('{}/__main__.py'.format(args.temdir), '{}/swagger_server/__main__.py'.format(args.path))

for root, dirs, files in os.walk(args.path):
     for file in files:
        with open(os.path.join(root, file), "r+") as f:
            data = f.read()
            data = re.sub('8080', args.port, data)
            f.seek(0)
            f.write(data)