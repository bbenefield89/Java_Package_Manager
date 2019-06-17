import click
import json
import os
import pprint
import requests

from xml.dom.minidom import parse
from xml.etree.ElementTree import ElementTree, Element, SubElement


current_directory = os.path.dirname(os.path.realpath(__file__))
pp = pprint.PrettyPrinter(indent=4)


def main():
    for root, dirs, files in os.walk(current_directory):
        if 'pom.xml' in files:
            return get_maven_package()
        else:
            print('Could not find "pom.xml" file')


@click.command()
@click.option('--package', prompt='Package Name', help='Enter a valid package name that can be found on the "Maven Repository"')
def get_maven_package(package):
    response = requests.get('https://search.maven.org/solrsearch/select?q=mysql-connector-java&wt=json')
    content = json.loads(response.content)['response']['docs']
    for package in content:
        if package['a'] == 'mysql-connector-java':
            return parse_xml()


def parse_xml():
    xml_tree = ElementTree()
    xml_tree.parse(f'{current_directory}/pom.xml')
    dependecies_tag = xml_tree.find('{http://maven.apache.org/POM/4.0.0}dependencies')
    dependency_tags = dependecies_tag.getchildren()

    new_dependency = Element('{http://maven.apache.org/POM/4.0.0}dependency')
    
    new_group_id = SubElement(new_dependency, '{http://maven.apache.org/POM/4.0.0}groupId')
    new_group_id.text = 'groupId'

    new_artifact_id = SubElement(new_dependency, '{http://maven.apache.org/POM/4.0.0}artifactId')
    new_artifact_id.text = 'artifactId'

    dependecies_tag.append(new_dependency)

    xml_tree.write(f'{current_directory}/pom2.xml')


if __name__ == '__main__':
    main()