from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='review.rfsepolicy',
      version=version,
      description="RFSE Review settings package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['review'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'ecreall.helpers.upgrade',
          'collective.js.jqueryui',
          'iw.rejectanonymous',
          'plone.app.dexterity',
          'plone.app.versioningbehavior',
          'plone.app.referenceablebehavior',
          'plone.principalsource',
          'plone.app.workflowmanager',
          'xlwt',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
