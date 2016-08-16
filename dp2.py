#!/usr/bin/python3
import argparse
import subprocess
import textwrap

class dp2:

    def __init__(self, attributes):
        self.attributes = attributes
        self.update_dependency()

    def update_groupid(self, files):
        if attributes['new_groupid'] is not None:
            print("Updating groupId from {} to {}...".format(self.attributes['groupid'], self.attributes['new_groupid']), end="")

            command = 'xmlstarlet ed --inplace -u \'//dependency[artifactId=\"{}\"]/groupId\' -v \"{}\" {}'\
            .format(attributes['artifactid'], attributes['new_groupid'], files)

            subprocess.call(command, shell=True)

            print(" Done")

    def update_version(self, files):
        if attributes['new_version'] is not None:

            prefix = ''
            suffix = ''
            if (attributes['aliased_version'] == True):
                prefix = '\${'
                suffix = '}'

            print("Updating version to {}{}{}...".format(prefix[1], self.attributes['new_version'], suffix), end="")

            command = "xmlstarlet ed --inplace -u \'//dependency[artifactId=\"{}\"]/version\' -v \"{}{}{}\" {}"\
            .format(attributes['artifactid'], prefix, attributes['new_version'], suffix, files)

            subprocess.call(command, shell=True)

            print(" Done")

    def update_dependency(self):
        files = ''
        xml_files = self.attributes['xmlfiles']
        for xml_file in xml_files:
            files = files + xml_file + ' '

        print("\nUpdating dependency {} in [{}]\n".format(attributes['artifactid'], files))

        self.update_groupid(files)
        self.update_version(files)


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='Updates maven dependency.',
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=textwrap.dedent("\n----Usage examples----\nUpdating dependency to ${dep.version} alias:\n"\
                                    +"\tdp2 org.depname -v dep.version --aliased-version pom.xml\n\n"\
                                    +"Updating dependency to 1.0.0 version:\n"\
                                    +"\tdp2 org.depname -v 1.0.0 pom.xml\n\n"\
                                    +"Updating dependency to 1.0.0 and groupId from org to br.org:\n"\
                                    +"\tdp2 org.depname -v 1.0.0 -g br.org pom.xml\n"))

    parser.add_argument('dependency', help='Dependency as groupId.artifactId')
    parser.add_argument('-g', '--groupid', help='Updates groupId')
    parser.add_argument('-v', '--version', help='Updates version')
    parser.add_argument('--aliased-version', help='Used when version is aliased. Example: ${dep.version}', action='store_const', const=True)
    parser.add_argument('xmlfiles', nargs='+', help="XML files with dependency tags")

    args = parser.parse_args()
    return process_cmd_args(args)

def process_cmd_args(args):
    dependency = args.dependency
    i = dependency.rfind('.')

    attributes = {}
    attributes['groupid'] = dependency[:i]
    attributes['artifactid'] = dependency[i+1:]
    attributes['new_groupid'] = args.groupid
    attributes['new_version'] = args.version
    attributes['aliased_version'] =  (args.aliased_version is not None)
    attributes['xmlfiles'] = args.xmlfiles

    return attributes

attributes = parse_cmd_args()
dp2(attributes)
