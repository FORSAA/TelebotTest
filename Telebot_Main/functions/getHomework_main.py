import selenium.common.exceptions

from Telebot_Main.imports.import_all_main import *

def getHomework_main(login: str, password: str, date:str, photomode: bool):
    browser_options = Options()
    browser_options.add_argument("--headless=new")
    # browser_options.add_argument("--start-maximized")
    browser_options.add_argument("--window-size=1000,750")

    browser = webdriver.Chrome(options=browser_options)
    try:
        browser.get("https://e-school.obr.lenreg.ru/authorize/login")

        browser.implicitly_wait(20)
        school_name = browser.find_element(By.CLASS_NAME, "select2-selection__placeholder")
        login_box = browser.find_element(By.NAME, "loginname")
        password_box = browser.find_element(By.NAME, "password")
        login_button = browser.find_element(By.CLASS_NAME, "primary-button")
        school_name.click()
        school_name_input = browser.find_element(By.CLASS_NAME, "select2-search__field")
        school_name_input.send_keys('МОБУ "СОШ "ЦО "Кудрово"')
        browser.find_elements(By.CLASS_NAME, "org-name-data")[1].click()

        login_box.send_keys(login)
        password_box.send_keys(password)
        login_button.click()

        browser.implicitly_wait(20)

        try:
            browser.implicitly_wait(0.5)
            if (browser.current_url != 'https://e-school.obr.lenreg.ru/angular/school/studentdiary/'):
                browser.find_element(By.XPATH, '/html/body/div/div[1]/div[4]/nav/ul/li[4]/a').click()
                browser.find_element(By.XPATH, '/html/body/div/div[1]/div[4]/nav/ul/li[4]/ul/li[1]/a').click()
        except NoSuchElementException as NSEE:
            if (browser.current_url == 'https://e-school.obr.lenreg.ru/authorize/login' or browser.current_url == 'https://e-school.obr.lenreg.ru/asp/SecurityWarning.asp'):
                browser.find_element(By.XPATH, '/html/body/div/div[1]/div/div/div[2]/div/div[4]/div/div/div/div/button[2]').click()
            if (browser.current_url != 'https://e-school.obr.lenreg.ru/angular/school/studentdiary/'):
                browser.find_element(By.XPATH, '/html/body/div/div[1]/div[4]/nav/ul/li[4]/a').click()
                browser.find_element(By.XPATH, '/html/body/div/div[1]/div[4]/nav/ul/li[4]/ul/li[1]/a').click()

        browser.implicitly_wait(20)
        if (browser.current_url == 'https://e-school.obr.lenreg.ru/angular/school/studentdiary/'):
            desired_div = browser.find_element(By.XPATH, f"//span[contains(., '{date}')]").find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
            rows = desired_div.find_elements(By.XPATH, ".//tr[@class='ng-scope']")
            if(photomode == False):
                data = []
                for row in rows:
                    data.append([row.text])
                to_return = f"Расписание на {date}: \n\n"
                for item in data:
                    item_text = "\n".join(item)
                    item_text = item_text.split('\n')
                    lesson_number = item_text[0]
                    subject = item_text[1]
                    time_and_room = item_text[2]
                    task = item_text[3] if len(item_text) > 3 else ""
                    formatted_item = f"Урок №{lesson_number}: Предмет: {subject}\nВремя/Кабинет: {time_and_room}\nЗадание: {task}\n\n =====================\n\n"
                    to_return += formatted_item
            else:
                sleep(0.2)
                desired_div.find_element(By.XPATH, '..').find_element(By.XPATH, '..').screenshot('screenshot.png')
                print(f'Screenshoted!')
                to_return = 'screenshot'
                # sleep(15)
    except Exception as other_Exceptions:
        print(other_Exceptions)

    except NoSuchElementException as NSEE_Exception:
        print('NoSuchElementException!', 1)
        browser.quit()
        return 'При обработке запроса возникла ошибка! Возможно, не удалось зайти в ваш аккаунт. Проверьте ваш логин и пароль.'

    finally:
        browser.implicitly_wait(5)
        browser.find_element(By.XPATH, "//a[@href='JavaScript:Logout(true);']").click()
        browser.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()
        browser.quit()
        return to_return




if __name__ == '__main__':
    print(getHomework_main('ЗахаровЕ9', '5084433', generate_the_date(1)))



