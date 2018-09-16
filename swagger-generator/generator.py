# coding: utf-8

import yaml
from jsonmerge import Merger
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("ver", help="The version number of this API specification")
parser.add_argument("--host", help="The host & port of the API endpoint", default="localhost:8888")
parser.add_argument("--defpath", help="The path of the definition file", default="input/definitions.yaml")
parser.add_argument("--defcpath", help="The path of the common definition file", default="input/definitions_common.yaml")
# parser.add_argument("--output", help="The path of the generated swagger spec file", default="./api_swagger_specification.yaml")
args = parser.parse_args()

schema = {"properties": { "tags" : { "mergeStrategy": "append" }, "paths" : { "mergeStrategy": "objectMerge" } } }
merger = Merger(schema)

main_str_template = open('template/template_main.yaml','r').read()
crud_str_template = open('template/template_crud.yaml', 'r').read()
definitions_common = yaml.load(open(args.defcpath,'r'))
definitions = yaml.load(open(args.defpath,'r'))

main = yaml.load(main_str_template.replace('${VERSION}', args.ver).replace('${HOST}', args.host))
main = merger.merge(main, definitions_common)
main = merger.merge(main, definitions)
for key in definitions['definitions']:
    crud = yaml.load(crud_str_template.replace('${KEY}', key))
    main = merger.merge(main, crud)

# with open(args.output, 'w') as f:
#     f.write(yaml.dump(main))
print(yaml.dump(main))
