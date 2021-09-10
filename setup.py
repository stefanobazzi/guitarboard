import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="guitarboard",
    version="0.0.1",
    author="Stefano Bazzi",
    description="Play live guitar (or mic) in you shell with python.",
    long_description=long_description,
    url="https://github.com/stefanobazzi/guitarboard",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
