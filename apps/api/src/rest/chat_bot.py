from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Set the path to your Chrome driver executable
driver_path = '/path/to/chromedriver'

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(driver_path)

# Open chat.reddit.com
driver.get('https://chat.reddit.com')

# Find the login button and click it
login_button = driver.find_element_by_xpath('//button[contains(text(), "Log in")]')
login_button.click()

# Find the username and password input fields and enter your credentials
username_input = driver.find_element_by_name('username')
username_input.send_keys('your_username')

password_input = driver.find_element_by_name('password')
password_input.send_keys('your_password')

# Submit the login form
password_input.send_keys(Keys.RETURN)