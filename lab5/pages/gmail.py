import time
from selenium.webdriver.common.by import By
from .base import BasePage
from selenium.webdriver.support import expected_conditions as EC


class ComposeEmailPage(BasePage):
    TO_FIELD = (By.ID, ':sg')
    TO_FIELD_ALT1 = (By.ID, ':vs')
    TO_FIELD_ALT2 = (By.ID, ':p6')

    RECIPIENT_COMPLETION = (By.ID, ':sh')
    RECIPIENT_COMPLETION_ALT1 = (By.ID, ':vt')
    RECIPIENT_COMPLETION_ALT2 = (By.ID, ':10j')

    SUBJECT_FIELD_BY_NAME = (By.NAME, "subjectbox")
    SUBJECT_FIELD_BY_XPATH = (By.XPATH, "//input[@placeholder='Тема' or @placeholder='Subject']")

    BODY_FIELD_UA = (By.XPATH, "//div[@role='textbox' and @aria-label='Текст повідомлення']")
    BODY_FIELD_GENERIC = (By.XPATH,
                          "//div[contains(@class, 'Am') and contains(@class, 'editable') and @role='textbox']")

    SEND_BUTTON_CLASS = (By.XPATH, "//div[contains(@class, 'T-I') and contains(@class, 'aoO')]")
    SEND_BUTTON_UA = (By.XPATH, "//div[@role='button' and contains(@aria-label, 'Надіслати')]")
    SEND_BUTTON_EN = (By.XPATH, "//div[@role='button' and contains(@aria-label, 'Send')]")

    def enter_recipient(self, email):
        print("Attempting to find recipient field...")
        recipient_field = None

        for locator in [self.TO_FIELD, self.TO_FIELD_ALT1, self.TO_FIELD_ALT2]:
            try:
                recipient_field = self.wait_for_element(locator)
                if recipient_field:
                    print(f"Found recipient field with {locator}")
                    break
            except Exception as e:
                print(f"Selector failed: {locator}")
                continue

        if not recipient_field:
            raise Exception("Could not find recipient field")

        recipient_field.send_keys(email)
        time.sleep(3)

        try:
            for locator in [self.RECIPIENT_COMPLETION, self.RECIPIENT_COMPLETION_ALT1, self.RECIPIENT_COMPLETION_ALT2]:
                try:
                    self.wait_for_element(locator).click()
                    break
                except:
                    continue
        except:
            print("No recipient completion found, continuing")

        time.sleep(3)

    def enter_subject(self, subject):
        try:
            subject_field = self.wait_for_element(self.SUBJECT_FIELD_BY_NAME)
        except:
            subject_field = self.wait_for_element(self.SUBJECT_FIELD_BY_XPATH)
        subject_field.click()
        time.sleep(2)
        subject_field.send_keys(subject)
        time.sleep(5)

    def enter_body(self, body):
        try:
            email_body = self.wait_for_element(self.BODY_FIELD_UA)
        except:
            email_body = self.wait_for_element(self.BODY_FIELD_GENERIC)
        email_body.click()
        time.sleep(2)
        email_body.send_keys(body)
        time.sleep(5)

    def send_email(self):
        try:
            send_button = self.wait.until(EC.element_to_be_clickable(self.SEND_BUTTON_UA))
        except:
            send_button = self.wait.until(EC.element_to_be_clickable(self.SEND_BUTTON_CLASS))
        self.safe_click(send_button)
        time.sleep(15)


class InboxPage(BasePage):
    COMPOSE_BUTTON = (By.XPATH, '//div[@class="T-I T-I-KE L3"][@role="button"]')
    COMPOSE_BUTTON_ALT = (By.CSS_SELECTOR, "div.T-I.T-I-KE.L3")
    COMPOSE_BUTTON_TEXT = (By.XPATH, "//div[text()='Compose' or text()='Написати']")

    def compose_new_email(self):
        print("Looking for compose button...")
        for locator in [self.COMPOSE_BUTTON, self.COMPOSE_BUTTON_ALT, self.COMPOSE_BUTTON_TEXT]:
            try:
                compose_button = self.wait.until(EC.element_to_be_clickable(locator))
                print("Found compose button!")
                self.safe_click(compose_button)
                time.sleep(7)
                return ComposeEmailPage(self.driver)
            except Exception as e:
                print(f"Selector failed: {locator}, trying next...")
                continue

        raise Exception("Could not find compose button with any selector")


class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, 'identifierId')
    EMAIL_NEXT_BUTTON = (By.ID, 'identifierNext')
    PASSWORD_INPUT = (By.ID, 'password')
    PASSWORD_NEXT_BUTTON = (By.ID, 'passwordNext')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get('https://mail.google.com/mail/u/0/#inbox')

    def login(self, email, password):
        self.wait_for_element(self.EMAIL_INPUT).send_keys(email)
        next_button = self.wait.until(EC.presence_of_element_located(self.EMAIL_NEXT_BUTTON))
        self.wait_for_clickable(self.EMAIL_NEXT_BUTTON)
        self.safe_click(next_button)

        time.sleep(3)

        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)
        next_button = self.wait.until(EC.presence_of_element_located(self.PASSWORD_NEXT_BUTTON))
        self.wait_for_clickable(self.PASSWORD_NEXT_BUTTON)
        self.safe_click(next_button)
        time.sleep(2)
        return InboxPage(self.driver)
