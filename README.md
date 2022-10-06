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
**You will also have to install [GraphViz](https://graphviz.org/download/)**

Once you have installed dependencies, use

```console
$ pipenv shell
```

in order to activate the [virtual environment](https://docs.python.org/3/library/venv.html).

| Action                | Command                                                   |
| --------------------- | --------------------------------------------------------- |
| Run `__main__`        | `python -m prereq_flowchart`                              |
| Run a particular file | `python -m prereq_flowchart.<filename>`                   |
| Run all unit tests    | `python -m unittest discover -v -s tests/ -p "*test*.py"` |
| Format code           | `black .`                                                 |
| Check types           | `mypy prereq_flowchart/`                                  |
