import time
from cv2 import cv2
import pytesseract
from selenium import webdriver
import io
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Set pytesseract PATH
pytesseract.pytesseract.tesseract_cmd = r'C://Program Files//Tesseract-OCR//tesseract.exe'
# CONSTANTS
ID = "SRINIVAS@CAS.DRDO.IN"
PASSWORD = "SN@1086sa"
CAPTCHA = ""
GEM_URL = "https://sso.gem.gov.in/ARXSSO/oauth/doLogin"
SHORT_SLEEP_TIME = 3
MED_SLEEP_TIME = 10
in_bid = False

# 06-11-2023
def solve_captcha():
	# enter GEM Login Portal
	driver.get(GEM_URL)
	# enter your login Id
	loginBox = driver.find_element("xpath",'//*[@id ="loginid"]')
	loginBox.send_keys(ID)
	# locate and save the captcha
	image_binary = driver.find_element("xpath",'//*[@id="captcha1"]').screenshot_as_png # screenshot image
	img = Image.open(io.BytesIO(image_binary))	# read image
	img.save("images/captcha.png")	#save image
	# # decode captcha
	img = cv2.imread("images//captcha.png")
	captcha = pytesseract.image_to_string(img)
	# enter captcha
	captchaBox = driver.find_element("xpath",'//*[@id="captcha_math"]')
	captchaBox.send_keys(captcha)

# 06-11-2023
def enter_pass():
	passwordBox = driver.find_element("xpath",'//*[@id="password"]')
	passwordBox.send_keys(PASSWORD)
	submitBtn = driver.find_element("xpath", '//*[@id="arxLoginSubmit"]')
	submitBtn.click()

def close_crac_advisory():
	advisoryTickBox = driver.find_element("xpath",'//*[@id="bulk_payment_checkbox"]')
	advisoryTickBox.click()
	advisoryBox = driver.find_element("xpath", '//*[@id="bulk_payment_confirmation"]')
	advisoryBox.click()

#   Started on : 07-11-2023
# Completed on : 08-11-2023
def add_to_cart(current_item_url, current_qty):
	global in_bid
	driver.get(current_item_url)
	time.sleep(SHORT_SLEEP_TIME)
	# add to actual cart
	add_to_cart_btn = driver.find_element("xpath",'//*[@id="cart"]/input[4]')	# Add to Cart - Blue Button
	driver.execute_script("arguments[0].click();", add_to_cart_btn)
	time.sleep(SHORT_SLEEP_TIME)
	# Select Bid/RA Option for 1st time
	if not in_bid:
		try:
			driver.find_element("xpath",'/html/body/div[5]/div[3]/div/button[2]').click()
		except:
			driver.find_element("xpath",'/html/body/div[8]/div[3]/div/button[2]').click()
		in_bid = True
	time.sleep(SHORT_SLEEP_TIME)
	# # Close Advisory
	# tooltip = driver.find_element(By.XPATH,'//*[@id="ui-tooltip-20"]/div[2]/a')
	# driver.execute_script("arguments[0].click();", tooltip)
	time.sleep(SHORT_SLEEP_TIME)
	# Click on Proceed
	try:
		proceed_1 = driver.find_element("xpath",'/html/body/div[7]/div[3]/div/button')
	except:
		proceed_1 = driver.find_element("xpath",'/html/body/div[4]/div[3]/div/button')
	proceed_1.click()
	time.sleep(SHORT_SLEEP_TIME)
	# Auto-select golden parameters	
	driver.find_element("xpath",'//*[@id="all_filters_not_selected_dialogue"]/ul/l1[2]/input').click()
	time.sleep(2)
	# Click on Proceed-#2
	proceed_2 = driver.find_element("xpath",'html')
	try:
		proceed_2 = driver.find_element("xpath",'/html/body/div[8]/div[3]/div/button[2]')
	except:
		print("Element not found at div 8")
	try:
		proceed_2 = driver.find_element("xpath",'/html/body/div[10]/div[3]/div/button[2]')
	except:
		print("Element not found at div 10")
	try:
		proceed_2 = driver.find_element("xpath",'/html/body/div[11]/div[3]/div/button[2]')
	except:
		print("Element not found at div 11")
	proceed_2.click()	
	# wait for 10 seconds to load all the golden values
	time.sleep(MED_SLEEP_TIME)
	print("Golden Values Loaded")
	# Proceed with Golden Values Selected
	proceed_1.click()
	time.sleep(SHORT_SLEEP_TIME)
	# Proceed with default seller 
	try:
		driver.find_element("xpath",'/html/body/div[11]/div[3]/div/button[2]').click()
	except:
		driver.find_element("xpath",'/html/body/div[10]/div[3]/div/button[2]').click()
	time.sleep(SHORT_SLEEP_TIME)

	# Select the consignee and Item Quantity
	driver.find_element(By.XPATH,'//*[@id="select2-_consignee_data__consignee_post_id-container"]').click()
	driver.find_element(By.CLASS_NAME,"select2-search__field").send_keys("Sode Sri Ramana, Senior Stores Officer II, Medchal Malkajgiri, TELANGANA - 501301"+ Keys.ENTER)
	driver.find_element("xpath",'//*[@id="_consignee_data__required_quantity"]').send_keys(current_qty) # Select the consignee
	driver.find_element("xpath",'//*[@id="delivery-location-based-search"]/input').click() # Close the cart
	time.sleep(SHORT_SLEEP_TIME)
	return

if __name__ == "__main__":
	# initilize selenium
	options = webdriver.ChromeOptions()	# run selenium with custom options
	options.add_experimental_option('excludeSwitches', ['enable-logging'])	# disable selenium error logs
	options.add_experimental_option("detach", True)	# stop the window from auto-close
	driver = webdriver.Chrome(options=options)
	driver.maximize_window()	# full screen to grab the captcha better
	# solve the captcha & enter the username
	solve_captcha()
	# enter the password
	enter_pass()
	# close the advisory
	close_crac_advisory()
	item_urls = [
		"https://mkp.gem.gov.in/oem-compatible-cartridge-consumable/006r01828/p-5116877-58009835258-cat.html#variant_id=5116877-58009835258",
		"https://mkp.gem.gov.in/oem-compatible-cartridge-consumable/006r01829/p-5116877-51069308395-cat.html#variant_id=5116877-51069308395",
		"https://mkp.gem.gov.in/oem-compatible-cartridge-consumable/006r01830/p-5116877-64861906396-cat.html#variant_id=5116877-64861906396",
		"https://mkp.gem.gov.in/oem-compatible-cartridge-consumable/006r01831/p-5116877-40772807341-cat.html#variant_id=5116877-40772807341"
		]
	for item_url in item_urls:
		add_to_cart(item_url,2)
	print("All Items Added to cart")