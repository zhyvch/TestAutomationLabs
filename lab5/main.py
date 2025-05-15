import os
from dotenv import load_dotenv
from selenium import webdriver

from lab5.pages.gmail import LoginPage


def main():
    load_dotenv()
    driver = webdriver.Safari()

    try:
        login_page = LoginPage(driver)
        inbox_page = login_page.login(os.getenv('LAB4_EMAIL'), os.getenv('LAB4_PASSWORD'))

        for i in range(1, 4):
            compose_page = inbox_page.compose_new_email()
            compose_page.enter_recipient(os.getenv('LAB4_EMAIL'))
            compose_page.enter_subject('Test mail')
            compose_page.enter_body(f'Selenium test email number {i}')
            compose_page.send_email()

    finally:
        driver.quit()


if __name__ == "__main__":
    main()