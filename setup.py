from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name="waveload",
        version="0.1.0",
        author="Vincent Caboara",
        author_email="vcaboara@duck.com",
        description="A Python library to load Workrave historystats data into various databases.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/vcaboara/waveload",  # Replace with your repo URL
        packages=['waveload'],  # Explicitly list your package
        package_dir={'waveload': 'waveload'}, # Tell setuptools where to find it
        install_requires=[],  # Add any runtime dependencies here
        python_requires=">=3.7",
    )

