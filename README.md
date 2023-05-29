# Autocomplete & search

## Usage
In the project suffix and prefix trees are used.
In order for the main ui to work, they need to be accessible.

Therefore, the first step is to install the project
### Installation
#### If using pdm
Create a virtual environment(if not already):
```bash
pdm venv create
```
Use the virtual environment:
```bash
pdm use
```
Install the project:
```bash
pdm install
```

#### If using pip
Create a virtual environment(if not already):
```bash
python3 -m venv venv
```

Use the virtual environment:
```bash
source venv/bin/activate
```

Install the project:
```bash
pip install -e .
```

If not all packages are loading, install them using:
```bash
pip install -r requirements.txt
```

### Running
Just run the `src/ui/ui.py` file:
```bash
python src/ui/ui.py
```

Now type some text in the bottom field.
When a word with the same begginning is found, it will be displayed in a popup as a suggestion.
If you click on the suggestion or press enter while focused(for example, using tab), the suggestion will be inserted into the text field.

To search for a word, type it in the top field and press the button.
All the matches will be highlighted.


## Contributing

Make sure to
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

before committing, as otherwise the pre-commit will fail
