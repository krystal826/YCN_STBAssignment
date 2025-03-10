from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
browser.get('https://www.visitsingapore.com/')
browser.maximize_window()
time.sleep(3)

# Handle the pop-up (click the Accept button)
try:
    accept_button = browser.find_element(By.XPATH, "//button[contains(text(), 'ACCEPT ALL')]")
    accept_button.click()
    print("Pop-up 'Accept' button clicked!")
except NoSuchElementException:
    print("No pop-up found or 'Accept' button not found.")
    time.sleep(3)

#1. Verify page title of home page
pageTitle = browser.title
expectedTitle = "Visit Singapore Official Site - Discover Singapore's Best Attractions"
if pageTitle == expectedTitle:
    print("Title correct")
else:
    print(f"Title wrong! Expected:'{expectedTitle}', but actual:'{pageTitle}'")

time.sleep(3)

#2a. 11 selections shown under "Neighbourhoods"
try:
    neighbourhood_span = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Neighbourhoods')]"))
    )
    print("Neighbourhood span element exists")
    actions = ActionChains(browser)
    actions.move_to_element(neighbourhood_span).perform()
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH,"//span[contains(text(), 'Neighbourhoods') and contains(@class, 'active')]"))
    )
    print("Neighbourhoods tab is now active!")
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='fullWidth']"))
    )
    clickable_links = browser.find_elements(By.XPATH, "//div[@class='fullWidth']//a")
    if clickable_links:
        if len(clickable_links) == 11:
                print(f"Exactly 11 clickable links found under Neighbourhoods.")
                for link in clickable_links:
                    print(link.get_attribute("href"))
        else:
            print(f"Found {len(clickable_links)} clickable links, but expected 11.")
    else:
        print("No clickable links found under Neighbourhoods.")

# 2b. Orchard Road is one of the selection
    try:
        orchard_road_link = browser.find_element(By.XPATH,"//div[@class='fullWidth']//a[contains(text(), 'Orchard Road')]")
        print("Orchard Road is one of the selections!")
    except NoSuchElementException:
        print("Orchard Road is not one of the selections.")

    #3. Verify and Visit Featured Neighbourhood page
    featured_neighbourhood = browser.find_element(By.XPATH,"//div[@class='fullWidth']//a[contains(text(), 'Featured Neighbourhoods')]")
    featured_neighbourhood.click()
    print("Featured Neighbourhood is clicked")

except NoSuchElementException:
    print("Neighbourhoods span element does not exist.")

time.sleep(5)

browser.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

#3a. Civic District is default selection (data-position is 0)
try:
    civic_district_default = browser.find_element(By.XPATH,"//div[@data-id='Civic District'][@data-position='0']")
    print("Civic District is correctly selected as the default")
except NoSuchElementException:
    print("Civic District is not highlighted or selected.")

#4. Select Marina Bay icon from map
try:
    marina_bay_icon = browser.find_element(By.XPATH,"//img[@alt='Marina Bay']")
    marina_bay_icon.click()
    print("Marina Bay icon is clicked on the map")
    marina_bay_selected = browser.find_element(By.XPATH, "//div[@data-id='Marina Bay'][@data-position='0']")
    print("Marina Bay is now being selected")
except NoSuchElementException:
    print("Marina Bay icon not found.")

#4a. Description of Marina Bay is shown
try:
    marina_bay_des = browser.find_element(By.XPATH,"//div[@data-id='Marina Bay'][@data-position='0']//p[contains(text(), 'Marina Bay')]")
    print("Marina Bay is correctly selected and description is displayed")
except NoSuchElementException:
    print("Marina Bay description not found or not selected.")

#5. Switch to select Sentosa
try:
    sentosa_icon = browser.find_element(By.XPATH,"//img[@alt='Sentosa']")
    sentosa_icon.click()
    print("Sentosa icon is clicked on the map")
    sentosa_selected = browser.find_element(By.XPATH, "//div[@data-id='Sentosa'][@data-position='0']")
    print("Sentosa is now being selected")
except NoSuchElementException:
    print("Sentosa icon not found.")

#5a. Both Sentosa and Marina Bay icon switch (chosen icon showing hover state, else showing default-state)
#Check status of Sentosa icon
image_src_sentosa = sentosa_icon.get_attribute("src")
if "/hover-state/" in image_src_sentosa:
    print("Sentosa icon is chosen and in red colour")
else:
    print("Sentosa icon is not chosen")
#Check status of Marina Bay icon
image_src_marina = marina_bay_icon.get_attribute("src")
if "/default-state/" in image_src_marina:
    print("Marina Bay icon is not chosen and successfully switch with Sentosa")
else:
    print("Marina Bay icon is not switched!!")
browser.execute_script("window.scrollBy(0, 300);")
time.sleep(2)

#6. Click Sentosa Find out more
try:
    sentosa_findOutMore = sentosa_selected.find_element(By.XPATH,".//a[contains(text(), 'Find Out More')]")
    sentosa_findOutMore.click()
    print("Sentosa Find Out More is clicked")
except NoSuchElementException:
    print("Find Out More link not found.")

#7. Select Ocean Restaurant from Where to Eat section
WhrToEat_section = browser.find_element(By.XPATH, "//stb-title-with-slider[contains(@aem-data, 'Where to Eat')]")
browser.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", WhrToEat_section)
print("Scrolled to 'Where to Eat' section.")
time.sleep(5)

try:
    right_arr = browser.find_element(By.XPATH,"//stb-title-with-slider[contains(@aem-data, 'Where to Eat')]//button[@class='stb-button_root__ihnjK stb-button_arrow-right__32pR_ stb-title-with-slider_next-button__1ui10 stb-title-with-slider_button__2ZqgC']")
    print("Located")
except NoSuchElementException:
    print("Fail to locate")

for i in range(2):
    print(f"Clicking the button {i + 1} time")
    right_arr.click()
    time.sleep(3)

#7a. Ocean Restaurant page opened in a new tab
ocean_res = browser.find_element(By.XPATH,"//a[@aria-label = 'Ocean Restaurant']")
ocean_res.click()
time.sleep(3)
WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
window_handles = browser.window_handles
browser.switch_to.window(window_handles[1])
time.sleep(3)

#7b. Close the tab and switch back to Sentosa page
browser.close()
browser.switch_to.window(window_handles[0])
time.sleep(3)

#8. Click search icon and type "Garden by the bay"
browser.execute_script("window.scrollTo(0, 0);")
time.sleep(3)
search_icon = browser.find_element(By.XPATH,"//div[@class='search-icon']")
search_icon.click()
print("Search icon clicked")
search_value = browser.find_element(By.XPATH,"//input[@placeholder='Search']")
search_value.send_keys("Garden by the bay")
print("Value entered")
search_value.send_keys(Keys.RETURN)
time.sleep(3)
first_search = browser.find_element(By.XPATH,"//a[contains(@href, 'gardens-by-the-bay')]")
first_search.click()
print("Clicked the first link")

#8a. There is breadcrumb navigation feature
try:
    breadcrumb = browser.find_element(By.XPATH,"//div[contains(@class, 'breadcrumbs')]")
    print("Breadcrumb navigation is present")
except:
    print("Breadcrumb navigation is not present on the page.")

#9. Click Marina Bay by breadcrumb
marina_bay_breadcrumb = breadcrumb.find_element(By.XPATH,".//a[contains(text(), 'Marina Bay')]")
marina_bay_breadcrumb.click()
print("Clicked on the 'Marina Bay' breadcrumb link.")

#9a. 4 mrt stations under "useful info"
useful_info_section = browser.find_element(By.XPATH, "//h2[contains(text(), 'Useful Information ')]")
browser.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", useful_info_section)
print("Scrolled to 'Useful Information' section.")
time.sleep(3)

mrt = browser.find_element(By.XPATH, "//div[@class='stb-typography_richText__pP-IR stb-typography_align-left__1yMpn stb-typography_richText__pP-IR rteContent stb-icon-text_description___vjjW']")
if useful_info_section != mrt and useful_info_section.is_displayed() and mrt.is_displayed():
    print("The 4 mrt are inside the Useful Information section.")
else:
    print("The 4 mrt are not inside Useful Information section.")

browser.quit()