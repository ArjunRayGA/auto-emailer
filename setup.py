from setuptools import setup, find_packages
setup(
    name="Auto-Mailer",
    version="0.1",
    packages=find_packages(),
    scripts=['say_hello.py'],

    # # Project uses reStructuredText, so ensure that the docutils get
    # # installed or upgraded on the target machine
    # install_requires=['docutils>=0.3'],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },

    # metadata for upload to PyPI
    author="Arjun Ray",
    author_email="deconstructionalism@gmail.com",
    # description="This is an Example Package",
    # license="PSF",
    keywords="gmail template email python",
    # url="http://example.com/HelloWorld/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)