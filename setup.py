from setuptools import setup, find_packages

setup(
    name='ShelfCMS',
    version='0.9.17',
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
        'Flask',
        'Flask-Admin',
        'Flask-Principal',
        'Flask-Security',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'humanize',
        'Jinja2',
        'py-bcrypt',
        'SQLAlchemy',
        'Werkzeug',
        'WTForms',
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
