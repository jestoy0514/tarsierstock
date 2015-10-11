from distutils.core import setup

setup(
    name='Tarsier Stock',
    version='0.1',
    packages=[''],
    url='http://jestoy0514.github.io/tarsierstock',
    license='GNU General Public License Version 2',
    author='Jesus Vedasto Olazo',
    author_email='jestoy.olazo@gmail.com',
    description='A simple stock management system.',
    options={'py2exe': {'bundle_files': 2}},
    zipfile=None,
    windows=[{
            "script": "tarsierstock.pyw",
            "icon_resources": [(1, "tsicon.ico")],
            "dest_base":"myprogram"
            }]
)
