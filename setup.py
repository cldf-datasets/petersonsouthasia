from setuptools import setup


setup(
    name='cldfbench_petersonsouthasia',
    py_modules=['cldfbench_petersonsouthasia'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'petersonsouthasia=cldfbench_petersonsouthasia:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
