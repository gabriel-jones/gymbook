from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


TIMEOUT = 10 # seconds

def book_slot(username, password, target_date, target_time):
	opts = webdriver.firefox.options.Options()
	opts.headless = True

	driver = webdriver.Firefox(options=opts)
	
	print("[~] Loading app...")
	driver.get('https://www.sport.ed.ac.uk/online-booking/Account/LogOn')

	try:
		# login
		username_input = driver.find_element_by_name('UserName')
		assert username_input is not None
		username_input.send_keys(username)

		password_input = driver.find_element_by_name('Password')
		assert password_input is not None
		password_input.send_keys(password)

		login_buttons = driver.find_elements(By.XPATH, '//input[@type="submit"]')
		assert len(login_buttons) == 1
		login_button = login_buttons[0]
		print("[~] Located login_button")
		login_button.click()
		print("[*] Logged in")

		print("[[========================]]")

		# enter search params
		search_for_radio = WebDriverWait(driver, TIMEOUT).until(
			EC.element_to_be_clickable((By.ID, "searchForActivity"))
		)
		print("[~:search_params] Located search_for_radio")
		search_for_radio.click()
		print("[~:search_params] Selected search for radio")

		search_location = Select(WebDriverWait(driver, TIMEOUT).until(
			EC.element_to_be_clickable((By.ID, "SiteID"))
		))
		print("[~:search_params] Located search_location")
		search_location.select_by_index(2) # pleasance
		print("[~:search_params] Selected pleasance location")

		search_activity = Select(WebDriverWait(driver, TIMEOUT).until(
			EC.element_to_be_clickable((By.ID, "Activity"))
		))
		print("[~:search_params] Located search_activity")
		time.sleep(0.5)
		search_activity.select_by_index(2) # gym access
		print("[~:search_params] Selected gym access activity")

		search_date = WebDriverWait(driver, TIMEOUT).until(
			EC.presence_of_element_located((By.ID, "SearchDate"))
		)
		print("[~:search_params] Located search_date")
		search_date.clear()
		search_date.send_keys(TARGET_DATE)
		print(f"[~:search_params] Selected date {TARGET_DATE}")

		driver.find_element_by_id("SearchCriteria").click()
		print("[~] Clicking away from date input")

		search_button = WebDriverWait(driver, TIMEOUT).until(
			EC.presence_of_element_located((By.CLASS_NAME, "NavigationButton"))
		)
		print("[~:search_params] Located search_button")
		time.sleep(0.5)
		search_button.click()
		print(f"[*:search_params] Search button clicked")

		print("[[========================]]")

		# parse search results
		print("[~] Loading search results...")
		search_results = WebDriverWait(driver, TIMEOUT).until(
			EC.presence_of_element_located((By.CLASS_NAME, "ActivitySearchResults"))
		)
		print("[*] Got search results")
		search_table = search_results.find_element_by_tag_name('tbody')
		assert search_table is not None
		print("[~] Located search_table")

		# find row at target time
		target_row = None
		search_rows = search_table.find_elements_by_tag_name('tr')
		assert len(search_rows) > 0
		print("[~] Located search_rows")

		for row in search_rows:
			row_time = row.find_element_by_class_name('TimeField')
			assert row_time is not None
			if row_time.text == TARGET_TIME:
				print(f"[*] Found target row at {TARGET_TIME}")
				target_row = row
				break

		assert target_row is not None

		# add to basket
		print("[~] Waiting for add to basket button...")
		add_basket_button = WebDriverWait(target_row, TIMEOUT).until(
			EC.presence_of_element_located((By.CLASS_NAME, "sr_AddToBasket"))
		)
		print("[~] Adding to basket...")
		add_basket_button.click()
		print("[*] Added to basket")

		print("[[========================]]")

		# checkout
		print("[~] Waiting for checkout...")
		checkout_button = WebDriverWait(driver, TIMEOUT).until(
			EC.presence_of_element_located((By.ID, "CheckoutSubmit"))
		)

		terms_checkbox = driver.find_element_by_id('TermsAccepted')
		print("[*] Located terms checkbox")
		terms_checkbox.click()

		print("[~] Located checkout button, submitting...")
		checkout_button.submit()
		print("[*] Checked out")

		print("[[========================]]")

		# confirm booking
		confirm_button_container = WebDriverWait(driver, TIMEOUT).until(
			EC.presence_of_element_located((By.CLASS_NAME, "CheckoutFoCLink"))
		)
		print("[~] Located confirm_button_container")
		confirm_button = confirm_button_container.find_element_by_tag_name('a')
		assert confirm_button is not None
		print("[~] Located confirm_button")
		# confirm_button.click()
		print("[*] Confirmed")

	except TimeoutException as e:
		print("[!] Timeout after 10 seconds")
		print(e)
	finally:
		print("[~] Quitting driver...")
		driver.quit()
