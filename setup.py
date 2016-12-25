from distutils.core import setup

setup(
    name='Tarsier Stock',
    version='0.2',
    packages=[''],
    url='http://jestoy0514.github.io/tarsierstock',
    license='GNU General Public License Version 2',
    author='Jesus Vedasto Olazo',
    author_email='jessie@jestoy.frihost.net',
    description='A simple stock management software.',
    options={'py2exe': {'bundle_files': 2}},
    zipfile=None,
    windows=[{
            "script": "tarsierstock.pyw",
            "icon_resources": [(1, "tsicon.ico")],
            "dest_base":"myprogram"
            }]
)
