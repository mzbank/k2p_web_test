# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from selenium import webdriver
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

#driver = webdriver.Chrome()
driver = webdriver.Firefox()
networkRestartTime = 40
rebootTime = 70

def openDriver():
	driver.get("http://p.to")
	driver.maximize_window()

def waitandClick(xpath):
	try:
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
	except TimeoutException as e:
		print('Error:waitandClick, TimeoutException, xpath = %s\n' % xpath)
		writewebErrToLog('waitandClick', 'TimeoutException', xpath)
		return False

	driver.find_element_by_xpath(xpath).click()

def waitandSendkeys(xpath, keys):
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
	except TimeoutException as e:
		print('Error:waitandSendkeys, TimeoutException, xpath = %s\n' % xpath)
		writewebErrToLog('waitandSendkeys', 'TimeoutException', xpath)
		return False

	driver.find_element_by_xpath(xpath).clear()
	driver.find_element_by_xpath(xpath).send_keys(keys)

def clickApp():
	time.sleep(1)
	waitforDisplay('//*[@id="Con"]/div[1]/ul[1]/a[4]/li')
	waitandClick('//*[@id="Con"]/div[1]/ul[1]/a[4]/li')
	waitforDisplay('//*[@id="Content"]')

def executeJS(js):
	driver.execute_script(js)

def srcollAction(site):
	scrollTop = '0'
	if site == 'top':
		scrollTop = '0'
	elif site == 'bottom':
		scrollTop = '10000'
	#web.executeJS("var q = document.getElementById('Content').scrollTop=10000")
	driver.execute_script("var q = document.getElementById('Content').scrollTop=%s" % scrollTop)

def alwaysOpenSwitch(xpath, switchValue='data-value'):
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
	button = driver.find_element_by_xpath(xpath)
	if button.get_attribute(switchValue) == '0':
		button.click()

def alwaysCloseSwitch(xpath, switchValue='data-value'):
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
	button = driver.find_element_by_xpath(xpath)
	if button.get_attribute(switchValue) == '1':
		button.click()

def closeDriver():
	#time.sleep(15) 
	time.sleep(1)
	driver.quit()
	os.system('killall chromedriver')

def refresh():
	driver.refresh()

def waitforDisappear(xpath):
	waitforDisplay(xpath)
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
	except TimeoutException as e:
		print('Error:waitforDisappear, TimeoutException, xpath = %s\n' % xpath)
		writewebErrToLog('waitforDisappear', 'TimeoutException', xpath)
		return False

	try:
		process = driver.find_element_by_xpath(xpath)
		WebDriverWait(driver, 20).until_not(lambda driver: process.is_displayed())
	except NoSuchElementException as e:
		print('Error:waitforDisappear, NoSuchElementException, xpath = %s\n' % xpath)
		writewebErrToLog('waitforDisappear', 'NoSuchElementException', xpath)
		return False

def waitforDisplay(xpath):
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
	except TimeoutException as e:
		print('Error:waitforDisplay, TimeoutException, xpath = %s\n' % xpath)
		writewebErrToLog('waitforDisplay', 'TimeoutException', xpath)
		return False

	try:
		process = driver.find_element_by_xpath(xpath)
		WebDriverWait(driver, 10).until(lambda driver: process.is_displayed())
	except NoSuchElementException as e:
		print('Error:waitforDisplay, NoSuchElementException, xpath = %s\n' % xpath)
		writewebErrToLog('waitforDisplay', 'NoSuchElementException', xpath)
		return False

def elementIsDisplayed(xpath):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException as e:
		return False
	return True

def getElementInTable(tableXpath, baseXpath, arrData,):
	table = driver.find_element_by_xpath('//*[@id="PortfwdTab"]')
	#table的总行数，包含标题
	table_rows = len(table.find_elements_by_tag_name('tr'))
	#tabler的总列数
	table_cols = len(arrData) - 1
	flag = False
	for row in range(2,table_rows + 1):
		for col in xrange(1,table_cols + 1):
			xpath = '%s/tr[%d]/td[%d]' %(baseXpath, row, col)
			if arrData[col] == driver.find_element_by_xpath(xpath).text:
				if col == table_cols:
					flag = True
			else:
				break
		if flag == True:
			return row
	return 0





