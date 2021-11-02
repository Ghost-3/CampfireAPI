import setuptools

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["requests<=2.26.0"]

setuptools.setup(
    name="Campfire API",
    version="0.0.1",
    author="Ghost-3",
    # Его почта.
    author_email="ghost3.github@gmail.com",
    description="CampfireAPI based on Capfire web.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ghost-3/CapfireAPI",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
