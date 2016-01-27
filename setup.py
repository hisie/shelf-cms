from setuptools import setup, find_packages

setup(
    name='ShelfCMS',
    version='0.9.11',
    url='https://github.com/iriahi/shelf-cms',
    license='BSD',
    author='Ismael Riahi',
    author_email='ismael@batb.fr',
    description="""Enhancing flask microframework with beautiful admin
                and cms-like features""",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-admin',
        'flask-wtf',
        'flask-security',
        'flask-sqlalchemy',
        'wtforms',
        'py-bcrypt'
    ]
)
