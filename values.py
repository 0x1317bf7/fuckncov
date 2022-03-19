USERNAME = "USERNAME"
username = None

PASSWORD = "PASSWORD"
password = None

WEB_LOGIN = "WEB_LOGIN"
web_login = None

ADDRESS = "ADDRESS"
address = None

USERAGENT = "USERAGENT"
useragent = None

DAY_OF_WEEK = "DAY_OF_WEEK"
day_of_week = None

TIME = "TIME"
time = None

debug = False

from urllib.parse import quote
import os


def init() -> None:
    global username
    global password
    global address
    global useragent
    global day_of_week
    global time
    global web_login

    username = os.environ.get(USERNAME)
    password = os.environ.get(PASSWORD)

    if username is None or password is None:
        if username is None or username == "":
            print("username is empty")
        if password is None or password == "":
            print("username is empty")
        raise AttributeError("username or password is empty")

    address = os.environ.get(ADDRESS)
    if address is not None:
        address = quote(address)

    time = os.environ.get(TIME)
    if time is None:
        time = "14:10"

    day_of_week = os.environ.get(DAY_OF_WEEK)
    if day_of_week is None:
        day_of_week = "0-6"

    web_login = os.environ.get(WEB_LOGIN)
    if web_login is None:
        web_login = False
    else:
        web_login = web_login.lower() == "true"

    useragent = os.environ.get(USERAGENT)
    if useragent is None:
        useragent = "Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Tablet/15E148 Safari/604.1"

    print(username)
    print(password)
    print(address)
    print(web_login)
    print(day_of_week)
    print(time)
    print(useragent)
