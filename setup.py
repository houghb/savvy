try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

opts = dict(name='savvy',
            description='Sensitivity analysis visualization tools',
            long_description='Interactive tools to visualize high '
                             'dimensionality sensitivity analysis results '
                             'generated using SALib (or similar).',
            license=open('LICENSE').read(),
            author='houghb, cdf6gc, swapilpaliwal',
            packages=['savvy', 'savvy/tests'],
            package_data={'savvy': ['sample_data_files/*.*',
                    'sample_data_files/without_second_order_indices/*.*']},
            include_package_data=True
            )


if __name__ == '__main__':
    setup(**opts)
