# Setting up the project
First things first: setting up the project. In this exercise we will focus on a single way to set up a project. Namely, we'll use [UV](https://docs.astral.sh/uv/). The main reason why we provide you with UV is because it is fast, scalable, and combines multiple tools into a single package. So let's get started!

## Installing UV
UV is an extended alternative to pip, which might be more familiar to anyone who has used Python before. However, UV offers more while still supporting everything pip does. It combines or replaces pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more.

To install:

<details>
<summary><strong>macOS & Linux</strong></summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# or

brew install uv
```

</details>

<details>
<summary><strong>Windows</strong></summary>

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

</details>

<br />

After successfully installing UV it should be available as a command. We are going to test it by running the command with the `--version` option.

```bash
uv --version
```

The output should look something like: **uv 0.9.26**

## Python version
Throughout this workshop we will use Python 3.12.x to ensure compatibility and consistency across the workshop environment.

Instead of installing Python manually, we will let UV manage the Python installation for us.

First install Python using UV:

```bash
uv python install 3.12
```

---

# Setting up the game project

<details>
<summary><strong>Initializing project</strong></summary>

UV will manage our project dependencies and environments.  

To set up a project, UV provides the `init` command.

The `uv init` command can be run without a parameter, in which case it will use the current folder to set up the project, or with a parameter, which will create a new folder inside your current working directory and initialize the project there.

We will initialize the project in **package mode** so our project can be installed automatically.

```bash
uv init --package {GAMENAME}

cd {GAMENAME}
```

Now pin the Python version for the project:

```bash
uv python pin 3.12
```

Next we ill create the main.py file:

```bash
touch main.py
```

The folder should look like this. It still misses a few important files and folders, but we will add those.

```
{GAMENAME}/
├── .python-version
├── main.py
├── pyproject.toml
├── src/
│   └── {GAMENAME}/
│       └── __init__.py
└── README.md
```

The **.python-version** file specifies the Python version used for this project.  
The **main.py** file, as the name implies, is our main file that we will use to run our game.  
The **pyproject.toml** file is the most important configuration file. In it we manage our project's metadata and dependencies.

</details>

---

<details>
<summary><strong>Adding libraries</strong></summary>

When adding a third-party library, it almost always installs more libraries than requested. This is something you should always take into account when importing a library.

To make sure you can trust a library and that it does not have a dependent library that could be malicious, try to find it on [PyPI](https://pypi.org/) first. If it is available there, the odds are that you are safe. You can also analyze more information about a library there, such as supported versions, license information, GitHub statistics, and more.

The `src` folder and package should already exist because we initialized the project in package mode.

We will now add our first dependency:

```bash
uv add python-dotenv
```

After adding a library, two things should appear in the project folder.

```
{GAMENAME}/
├── .venv
├── ...
└── uv.lock
```

The **.venv** folder contains the local virtual environment for this project. This is generated automatically and normally should not be modified manually.

The **uv.lock** file contains the locked versions of the required libraries for this project, as well as all libraries required by those libraries, and so on.

</details>

---

<details>
<summary><strong>Creating the environment</strong></summary>

We still miss the virtual environment, a key component of the Python architecture.

To create the virtual environment and install all dependencies, run:

```bash
uv sync
```

This command will:

- Create the `.venv` virtual environment
- Install all dependencies
- Install the local project package

</details>

---

<details>
<summary><strong>Importing and Running</strong></summary>

Now we will start by adding a file and a simple function to our package.

Navigate to the package directory:

```bash
cd src/{GAMENAME}
```

Create a new file:

```bash
touch board.py
```

Within `board.py`, add the function below. This function we will use to set up a basic unit test.

```python
def modulo(x: int, y: int) -> int:
    return x % y
```

Now open `main.py` and add the following code:

```python
from {GAMENAME} import board

if __name__ == "__main__":
    print(board.modulo(11, 4))
```

Now we can run this directly from the terminal while being in the main `{GAMENAME}` folder by running:

```bash 
uv run main.py
```

Et voilà! It should print **3**, the correct remainder of `11 % 4`.

</details>

---

<details>
<summary><strong>Unit testing</strong></summary>

Finally there is the `tests` folder. This folder will be used to store all our tests.

For testing there are two main libraries: `unittest` and `pytest`. Both are complementary to each other. This means that it could happen that you need both to run a test. However, we will showcase `pytest` here because it is better for larger projects and is more common.

First let's install the library:

```bash
uv add pytest
```

Then create a test file. It's important to prefix the file with `"test_"`. This makes pytest interpret it as a testable Python file.

```bash
mkdir tests
cd tests
touch test_board.py
```

Add this to the new test file:

```python
from {GAMENAME}.board import modulo

def test_sum_numbers():
    assert modulo(11, 1) == 0
    assert modulo(1, 11) == 1
    assert modulo(11, 3) == 2
    assert modulo(-1, 3) == 2
```

Finally let's test it:

```bash
uv run pytest
```

</details>

---

You made it through the first exercise! Congratulations! You now have a basic understanding of how to set up a Python project using _UV_. You can now move on to the next exercise. In the next exercise you will implement a basic game to learn more about the Python ecosystem.