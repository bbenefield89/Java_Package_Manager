import click
import json
import os
import pprint
import requests
import xml.etree.ElementTree as ElementTree


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
            return add_maven_package(package['g'], package['a'])


def add_maven_package(groupId, artifactId):
    ElementTree.register_namespace('', 'http://maven.apache.org/POM/4.0.0')
    xml_tree = ElementTree.ElementTree()
    xml_tree.parse(f'{current_directory}/pom.xml')
    dependecies_tag = xml_tree.find('{http://maven.apache.org/POM/4.0.0}dependencies')

    last_dependency_tag = dependecies_tag.findall('{http://maven.apache.org/POM/4.0.0}dependency')
    last_dependency_tag[-1].tail = '\n    '

    new_dependency = ElementTree.Element('{http://maven.apache.org/POM/4.0.0}dependency')
    new_dependency.text = '\n      '
    new_dependency.tail = '\n  '
    
    new_group_id = ElementTree.SubElement(new_dependency, '{http://maven.apache.org/POM/4.0.0}groupId')
    new_group_id.text = f'{groupId}'
    new_group_id.tail = '\n      '
    
    new_artifact_id = ElementTree.SubElement(new_dependency, '{http://maven.apache.org/POM/4.0.0}artifactId')
    new_artifact_id.text = f'{artifactId}'
    new_artifact_id.tail = '\n    '
    
    dependecies_tag.append(new_dependency)
    
    xml_tree.write(f'{current_directory}/pom.xml', encoding='UTF-8', xml_declaration=True)


if __name__ == '__main__':
    main()