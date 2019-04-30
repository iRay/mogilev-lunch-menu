### Mogilev Lunch Menu Telegram Bot

#### Requirements
```bash
python ^3.6
poetry
```

`pyenv` can be used to install needed version of python e.g.:

```bash
$ pip install pyenv
$ pyenv install 3.7.1
```

#### Installation
```bash
$ python -m venv ./venv
$ . ./venv/bin/activate
(venv)$ poetry install
```

ChromeDriver installation:
```bash
$ LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
$ wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip && sudo ln -s $PWD/chromedriver /usr/local/bin/chromedriver
$ export PATH=$PATH:/usr/local/bin/chromedriver
```