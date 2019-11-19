import pip
import os
import subprocess
import click
import json

import pip_api

# noinspection PyProtectedMember
from pip._internal.main import main as pip_main

REQUIREMENTS_FILE_PATH = 'requirements.json'


def get_requirements_from_file():
    if os.path.isfile(REQUIREMENTS_FILE_PATH):
        f = open(REQUIREMENTS_FILE_PATH, 'r')
        requirements_file_data = json.loads(f.read())
        return requirements_file_data.get('requirements', False)


def set_requirement(package, version):
    if os.path.isfile(REQUIREMENTS_FILE_PATH):
        f = open(REQUIREMENTS_FILE_PATH, 'r')

        requirements_file_data = json.loads(f.read())
        requirements = requirements_file_data.get('requirements', False)

        if requirements:
            requirements_file_data['requirements'][package] = version
        else:
            requirements_file_data['requirements'] = {package: version}

        f.close()

        f = open(REQUIREMENTS_FILE_PATH, 'w')
        f.write(json.dumps(requirements_file_data, indent=2))
        f.close()


def get_package_version(package):
    dists = pip_api.installed_distributions()

    package_info = dists.get(package, False)
    if package_info:
        return package_info.version.public

    package_info = dists.get(package.title(), False)
    if package_info:
        return package_info.version.public

    return False


def install_package(package_names):
    command = ['install']
    for package in package_names:
        command.append(package)

    pip_main(command)


def install_from_cli(packages, save):

    install_package(packages)

    for package in packages:
        package_name = package
        version = None

        if '==' in package:
            package_name, version = package.split('==')

        if save:
            installed_version = get_package_version(package_name)
            if installed_version:
                set_requirement(package_name, installed_version)


def install_from_req_file():
    requirements = get_requirements_from_file()
    packages = []

    if requirements:
        for name, version in requirements.items():
            if version:
                packages.append(f"{name}=={version}")
            else:
                packages.append(name)

        install_package(packages)


@click.group()
def cli():
    pip_majon_version = int("".join(pip.__version__.split('.')))
    if not pip_majon_version > 1800:
        click.echo(f'Your pip version is outdated, which is {pip.__version__}. Required pip version is 18.0.0 or newer.')
        exit()


@click.command()
@click.option('-S', '--save/--no-save', 'save', default=False)
@click.option('-U', '--upgrade', 'upgrade', default=False)
@click.argument('packages', nargs=-1, type=click.STRING, required=False)
def install(packages, save, upgrade):
    """ Installs given package[s]"""
    if not packages:
        install_from_req_file()
    else:
        install_from_cli(packages, save)


@click.command()
@click.argument('packages', nargs=-1, type=click.STRING)
def uninstall(packages):
    """Uninstalls given package[s]"""
    for package in packages:
        pip_main(['uninstall', package])


@click.command()
def init():
    """Initializes requirements.json file """
    if os.path.isfile(REQUIREMENTS_FILE_PATH):
        click.echo('Requirements file already initialized.')

    pwd = os.getcwd().split('/')[-1]
    project_name = input(f'Project name: ({pwd}) ') or pwd
    version = input('Version: (1.0.0) ') or "1.0.0"
    description = input('Description: ')
    author = input('Author: ')
    license_ = input('License: (ISC) ') or "ISC"

    init_json = {
        "name": project_name,
        "version": version,
        "description": description,
        "author": author,
        "license": license_
    }

    click.echo()
    click.echo(json.dumps(init_json, indent=2))
    click.echo()

    good = input('Looks good? (Y/n) ')
    if good == 'y' or good == 'Y' or good == '':
        f = open(REQUIREMENTS_FILE_PATH, 'w')
        f.write(json.dumps(init_json, indent=2))
        f.write('\n')


cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(init)
