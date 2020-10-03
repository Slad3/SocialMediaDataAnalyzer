from setuptools import setup

setup(
	name='Your Application',
	version='1.0',
	long_description=__doc__,
	packages=['flaskr'],
	include_package_data=True,
	zip_safe=False,
	install_requires=['Flask', 'Flask_CORS']
)