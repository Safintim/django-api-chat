from setuptools import setup

setup(
    name='django_api_chat',
    version='0.1',
    author='Timur Safin',
    author_email='timurtlt96@mail.ru',
    packages=['chat'],
    url='https://github.com/Safintim/django-api-chat',
    license='MIT',
    description='Django API chat',
    install_requires=['django', 'djangorestframework'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
        'Natural Language :: Russian',
    ]
)