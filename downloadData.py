from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

driver = webdriver.Edge()
driver.get("https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp")

dataClass = WebDriverWait(driver=driver, timeout=10).until(
    EC.presence_of_element_located((By.ID, "dataclass")))

dataInquery = dataClass.find_elements(By.TAG_NAME, "option")
dataInquery[0].click()

dataFormat = driver.find_element(By.ID, "datatype")
yearly_data = dataFormat.find_elements(By.TAG_NAME, "option")
yearly_data[2].click()

county = driver.find_element(By.ID, "stationCounty")
all_options_county = county.find_elements(By.TAG_NAME, "option")

for opt_c in all_options_county:
    # print("Value is: %s" % option.get_attribute("value"))
    opt_c.click()

    station = driver.find_element(By.ID, "station")
    all_options_station = station.find_elements(By.TAG_NAME, "option")

    count = 0
    for opt_s in all_options_station:
        if count >= 4:
            break

        opt_s.click()
        dataPicker = driver.find_element(By.ID, "datepicker")
        searchBtn = driver.find_element(By.ID, "doquery")
        for yearNum in range(1995, 2024):
            dataPicker.clear()
            dataPicker.send_keys(yearNum)
            searchBtn.click()

            currWH = driver.current_window_handle
            driver.switch_to.window(driver.window_handles[1])
            try:
                csv_download = WebDriverWait(driver=driver, timeout=10).until(
                    EC.presence_of_element_located((By.ID, "downloadCSV")))
            except Exception as ex:
                print(ex)
                print(
                    f"csv_download ERROR {opt_c.text} {opt_s.text} : {yearNum}"
                )
                driver.close()
                driver.switch_to.window(currWH)
                break

            csv_download.click()

            driver.close()
            driver.switch_to.window(currWH)

            # time.sleep(10)  # for test
        count += 1

driver.quit()
