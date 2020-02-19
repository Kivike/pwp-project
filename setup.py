from setuptools import find_packages, setup

#Solution from lovelace 
#https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-summer-2019/flask-api-project-layout/#making-the-project-installable

setup(
    name="game_score_api",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "SQLAlchemy",
    ]
)