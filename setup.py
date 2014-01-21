from setuptools import setup, find_packages
import os

version = '1.3'

setup(name='collective.portlet.shelf',
      version=version,
      description="collective.portlet.shelf is a portlet for Plone 4 "
          "that allows to display Collection's results in a carousel "
          "portlet browsing them by subcollections.",
      long_description=open("README.rst").read() + "\n" +
      open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='plone portlet shelf',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='https://github.com/collective/collective.portlet.shelf',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
