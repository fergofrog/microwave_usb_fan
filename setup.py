from setuptools import setup


install_requires = [pkg.strip() for pkg in open('requirements.txt').readlines()]

setup(name='microwave-usbfan',
      version='1.2',
      description="Rebranded UF-211-06RGB USB fans by USTAR (Ruishengda) protocol implementation",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/fergofrog/microwave_usb_fan',
      author='Fergus Symon',
      author_email='45412+fergofrog@users.noreply.github.com',
      license='MIT',
      packages=['usbfan'],
      include_package_data=True,
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: BSD',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Communications',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      )
