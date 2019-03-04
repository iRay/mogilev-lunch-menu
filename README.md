### Mogilev Lunch Menu Telegram Bot

ChromeDriver installation:
```bash
$ LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
$ wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip && sudo ln -s $PWD/chromedriver /usr/local/bin/chromedriver
$ export PATH=$PATH:/usr/local/bin/chromedriver
```