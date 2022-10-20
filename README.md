# prereq-flowchart

## First-time setup

We are using Python 3.10 and `pipenv`. Install Python 3.10 from [https://python.org](https://python.org).
Install `pipenv` with the following command:
```console
$ python3.10 -m pip install --user pipenv
```

Then, install dependencies:

```console
$ pipenv install
```

Once you have installed dependencies, use

```console
$ pipenv shell
```

in order to activate the [virtual environment](https://docs.python.org/3/library/venv.html).

| Action                  |  Command  |
|-------------------------|-----------|
|  Run `__main__`         | `python -m prereq_flowchart`  |
|  Run a particular file  | `python -m prereq_flowchart.<filename>`  |
|  Run all unit tests     | `python -m unittest discover -v -s tests/ -p "*test*.py"`  |
|  Format code            | `black .` |
|  Check types            | `mypy prereq_flowchart/` |

## Web scraping

We are using Selenium with Firefox, which requires the presence of geckodriver on your system and in your path/environment variables. You will also need to install Firefox separately.

You may add geckodriver to your path temporarily or permanently. Note that any execution of code that does scraping will need to access this environment variable, meaning it will need to be redeclared before every execution.

1. Go to this release page and download the corresponding package for your system
https://github.com/mozilla/geckodriver/releases
2. Put the executable somewhere safe (the project folder is not recommended) 
3. Add its path to your global PATH using one of the following procedures:

### Temporary

You will need to format your python executions to be of this format in order to load the environment variable every time.

Linux/macOS:

bash: `env GECKO=/path/to/folder/containing/executable python myScript.py`

Windows:

Note: if you have Git for Windows installed, you can use Git Bash, which would allow you to mostly follow the steps for Linux/macOS instead

PowerShell: `ah whatever`

### Permanent

Linux/macOS:

`PATH=$PATH:/path/to/folder/containing/executable`

Windows:

Note: if you have Git for Windows installed, you can use Git Bash, which would allow you to mostly follow the steps for Linux/macOS instead

Settings > System > About > Advanced System Settings > Environment Variables... > System Variables

Select PATH and click Edit...

Click new, add your path to the list