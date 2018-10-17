# coding: utf-8

import yaml
from jsonmerge import Merger
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("ver", help="The version number of this API specification")
parser.add_argument("--name", help="Tha name of the API service", default="JobSystemAPI")
parser.add_argument("--host", help="The host & port of the API endpoint", default="localhost:8888")
parser.add_argument("--basepath", help="The base path of the API endpoint", default="v1")
parser.add_argument("--definitions", help="The content of the definitions")
parser.add_argument("--output", help="The name of the generated swagger spec file", default="api_swagger_specification.yaml")
args = parser.parse_args()

schema = {"properties": { "tags" : { "mergeStrategy": "append" }, "paths" : { "mergeStrategy": "objectMerge" } } }
merger = Merger(schema)

main_str_template = open('etc/spec/template_main.yaml','r').read()
crud_str_template = open('etc/spec/template_crud.yaml', 'r').read()
definitions_common = yaml.load(open('etc/spec/definitions_common.yaml','r'))
definitions = yaml.load(args.definitions)

main = yaml.load(main_str_template.replace('${VERSION}', args.ver).replace('${HOST}', args.host).replace('${BASE_PATH}', args.basepath).replace('${NAME}', args.name))
main = merger.merge(main, definitions_common)
main = merger.merge(main, definitions)
for key in definitions['definitions']:
    crud = yaml.load(crud_str_template.replace('${KEY}', key))
    main = merger.merge(main, crud)

with open('etc/' + args.output, 'w') as f:
    f.write(yaml.dump(main))
