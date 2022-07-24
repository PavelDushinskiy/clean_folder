from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='0.0.2',
      description='Our first Package',
      author='Pavlo Dushinsky',
      author_email='Pavel.Dushinskiy@sysfx.com',
      license='MIT',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean=clean_folder.clean:main']}
)
