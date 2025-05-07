from dataclasses import dataclass
from abc import ABC

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Safari


@dataclass
class BasePage(ABC):
    driver: WebDriver


@dataclass
class BaseSafariPage(ABC, BasePage):
    driver: Safari
