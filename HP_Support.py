from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from selenium.common.exceptions import NoSuchElementException

def Sign_In_Notifications(id_username, id_password):
    driver.get('https://h30434.www3.hp.com/t5/notificationfeed/page')

    username = driver.find_element_by_id("username")
    username.send_keys(id_username)

    next_button = driver.find_element_by_id("next_button")
    next_button.click()

    time.sleep(1)
    password = driver.find_element_by_id("password")
    password.send_keys(id_password)

    submit_button = driver.find_element_by_css_selector("button[type='submit']")#driver.find_element_by_class_name("vn-button vn-button--critical vn-button--expanded")
    submit_button.click()

    driver.implicitly_wait(10)
    accept = driver.find_element_by_id('onetrust-accept-btn-handler')
    accept.click()
    '''
    try:
        accept = driver.find_element_by_id('onetrust-accept-btn-handler')
        accept.click()
    except NoSuchElementException:
        pass
    '''
    
    '''
    driver.implicitly_wait(10)
    accept = driver.find_element_by_id('onetrust-accept-btn-handler')
    accept.click()
    '''

    driver.implicitly_wait(10)
    notification_list = driver.find_element_by_id("notificationList")
    ul = notification_list.find_element_by_xpath(".//ul")

    unread_mention_list = ul.find_elements_by_xpath(".//li[@class='lia-notification-feed-item lia-notification-mentions lia-component-notificationfeed-widget-notification-feed-item']") #later change to unread and lia-notification-feed-item lia-notification-board lia-notification-unread lia-component-notificationfeed-widget-notification-feed-item NOPE change to lia-notification-feed-item lia-notification-mentions lia-notification-unread lia-component-notificationfeed-widget-notification-feed-item
    #lia-notification-feed-item lia-notification-board lia-component-notificationfeed-widget-notification-feed-item

    for mention in unread_mention_list:
        user = mention.find_element_by_xpath(".//div/div/div[2]/div/span").text
        if user == 'EddyK': 
            forum_thread_link = mention.find_element_by_xpath(".//div/div/div[2]/div/a")
            forum_thread_link.send_keys(Keys.CONTROL + Keys.ENTER)
            driver.switch_to.window(driver.window_handles[1])
            Identify_Commands()
        else:
            #do something

#Always call Main_Product_Page
def Main_Product_Page(model_name):
    #driver.execute_script('''window.open("https://support.hp.com/us-en/products","_blank");''')

    #driver.switch_to.window(driver.window_handles[2])

    driver.get('https://support.hp.com/us-en/products')

    driver.implicitly_wait(10)
    accept = driver.find_element_by_id('onetrust-accept-btn-handler')
    accept.click()

    search_box = driver.find_element_by_id('search-input-pfinder')
    search_box.send_keys(model_name)

    find_button = driver.find_element_by_id('btnSplitSearchSubmit')
    find_button.click()

    driver.implicitly_wait(10)
    full_product_name = driver.find_element_by_xpath("//div[@id='pdpPrdctHeading']/h2").text

    x_button = driver.find_element_by_id("dismiss-notifications")
    x_button.click()

    #<p><font size="6"><strong><font face="hpsimplifiedlight,arial,sans-serif">HP Spectre x360 - 13-ap0053dx</font></strong></font></p>
    answer += '<p><font size="6"><strong><font face="hpsimplifiedlight,arial,sans-serif">%s</font></strong></font></p>' % full_product_name

    return full_product_name, driver.current_url

def Product_Specifications(model_name):
    #driver.switch_to.window(driver.window_handles[2])

    product_information = driver.find_element_by_id('tab-product-info')
    product_information.click()

    driver.implicitly_wait(10)
    dropdown = driver.find_element_by_id("dd-727118134876361637267272859691104_dd_headerLink")
    driver.execute_script("arguments[0].scrollIntoView();", dropdown)
    driver.execute_script("arguments[0].click();", dropdown)

    dropdown_product_specifications = driver.find_element_by_xpath("//ul[@id='dd-727118134876361637267272859691104_dd_list']/li[2]/a")
    dropdown_product_specifications.click()

    driver.implicitly_wait(10)
    product_specifications_text = driver.find_element_by_xpath("//div[@id='dd-items_727118134876361637267272859691104']/div/ul/li/a/*[contains(text(), '%s')]" % model_name)
    driver.execute_script("arguments[0].scrollIntoView();", product_specifications_text)
    driver.execute_script("arguments[0].click();", product_specifications_text)
    #product_specs_page = product_specifications_text.find_element_by_xpath('..')
    #product_specs_page.click()

    driver.switch_to.window(driver.window_handles[1])

    product_specs_url = driver.current_url

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

    return product_specs_url

def Maintenance_and_Service_Guide():
    #driver.switch_to.window(driver.window_handles[2])

    manuals = driver.find_element_by_id('manuals')
    manuals.click()

    maintenance_and_service_guide_text = driver.find_element_by_xpath("//tbody[@id='userGuidesList']/tr/td/a/*[contains(text(), 'Maintenance and Service Guide')]")
    driver.execute_script("arguments[0].scrollIntoView();", maintenance_and_service_guide_text)
    driver.execute_script("arguments[0].click();", maintenance_and_service_guide_text)
    maintenance_and_service_guide_page = maintenance_and_service_guide_text.find_element_by_xpath('..').get_attribute('href')
    
    driver.switch_to.window(driver.window_handles[1])

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

    #<hr /><p><font size="5"><strong>Maintenance and Service Guide</strong></font></p>

    return maintenance_and_service_guide_page

def Identify_Commands():
    post_url = driver.current_url
    split_url = post_url.split("/")

    for url in split_url:
        if '#' in url:
            string_hash = url.split("#")
            post_number = string_hash[0]
            break 

    post = driver.find_element_by_xpath("//div[@data-lia-message-uid='%s']" % post_number)
    driver.execute_script("arguments[0].scrollIntoView();", post)
    reply_button = post.find_element_by_xpath(".//a[@class='lia-button lia-button-secondary reply-action-link lia-action-reply']")
    driver.execute_script("arguments[0].scrollIntoView();", reply_button)
    driver.execute_script("arguments[0].click();", reply_button)

driver = webdriver.Edge(r"C:\Users\EddyM\Downloads\edgedriver_win64 (1)\msedgedriver.exe")
#driver = webdriver.Firefox("C:\Users\EddyM\Downloads\geckodriver-v0.29.0-win64\geckodriver.exe")

Sign_In_Notifications(username, password)
model_name = "an015np"
full_product_name, main_product_page_url = Main_Product_Page(model_name)
print(Maintenance_and_Service_Guide())
print(Product_Specifications(model_name))
print("Success")
driver.quit()