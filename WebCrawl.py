# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 08:16:43 2023

@author: scorp
"""

from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json

main_logo = '//*[@id="Kroll_Main_Logo"]'
claim_forms = '//td[contains(@title,"Claim #")]/span/a'
claim_column = '//div[text()="Claim #"]'
cred_data_details_header = '//h1[contains(text(),"Creditor Data Details")]'

creditor_span = '//span[text()="Creditor"]'
main_address = '//address'
sub_address = '//address/br'

debtor_name = '//span[text()="Debtor Name"]'
debtor_name_data = '//span[text()="Debtor Name"]/following-sibling::span'

date_filed = '//span[text()="Date Filed"]'
date_filed_data = '//span[text()="Date Filed"]/following-sibling::span'

claim_number = '//span[text()="Claim Number"]'
claim_number_data = '//span[text()="Claim Number"]/following-sibling::span'

schedule_number = '//span[text()="Schedule Number"]'
schedule_number_data = '//span[text()="Schedule Number"]/following-sibling::span'

close_button = '//button[text()="Close"]'

claimed = '//*/span[contains(text(),"Total")]/parent::td/following-sibling::td/b[contains(text(),"Asserted Claim")]/following-sibling::span';


# Withdrar History
history_claim_date = '//*/h2[contains(text(),"Withdrawal History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Date Filed")]/following-sibling::span';
history_claim_text = '//*/h2[contains(text(),"Withdrawal History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Withdrawal Document")]/following-sibling::span';
history_claim_href = '//*/h2[contains(text(),"Withdrawal History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Withdrawal Document")]/following-sibling::span/a';
history_docket_number = '//*/h2[contains(text(),"Withdrawal History")]/parent::div/table/tbody/tr/td/b[text()="Docket Number"]/parent::td/span'


# Objection history
obj_date = '//*/h2[contains(text(),"Objection History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Date Filed")]/following-sibling::span';
obj_motion_text = '//*/h2[contains(text(),"Objection History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Objection Motion")]/following-sibling::span';
obj_motion_href = '//*/h2[contains(text(),"Objection History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Objection Motion")]/following-sibling::span/a';
obj_order_text = '//*/h2[contains(text(),"Objection History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Objection Order")]/following-sibling::span'
obj_order_href = '//*/h2[contains(text(),"Objection History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Objection Order")]/following-sibling::span/a'
obj_hist_basis = '//*/h2[contains(text(),"Objection History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Basis")]/following-sibling::span'
obj_hist_status = '//*/h2[contains(text(),"Objection History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Status")]/following-sibling::span'

# Stipulation History
stipulation_date = '//*/h2[contains(text(),"Stipulation History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Date Filed")]/following-sibling::span'
stipulation_docket_number = '//*/h2[contains(text(),"Stipulation History")]/parent::div/table/tbody/tr/td/b[text()="Docket Number"]/parent::td/span'
stipulation_doc_text = '//*/h2[contains(text(),"Stipulation History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Stipulation Document")]/following-sibling::span'
stipulation_doc_href = '//*/h2[contains(text(),"Stipulation History")]/parent::div/table/tbody/tr/td/b[contains(text(),"Stipulation Document")]/following-sibling::span/a'


next_button = '//*/span[contains(text(),"NEXT")]/parent::a'




driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

driver.get('https://cases.ra.kroll.com/seadrillpartners/Home-ClaimInfo');

title = driver.title
print(title)
# driver.quit()

# Set the maximum wait time (in seconds) for the element to be visible.
wait_time = 300

# Create a WebDriverWait instance, passing the driver and the maximum wait time.
wait = WebDriverWait(driver, wait_time)

wait.until(EC.visibility_of_element_located((By.XPATH, claim_column)))

main_json_data = {}

# check current page
total_page = driver.find_elements(By.XPATH,'//*[@id="p-total-pages"]')
current_page = driver.find_elements(By.XPATH,'//*[@id="pagenum"]')

# while(int(current_page[0].get_attribute("value")) != int(total_page[0].text)):
while(int(current_page[0].get_attribute("value")) != 10):
    
    wait.until(EC.visibility_of_element_located((By.XPATH, claim_column)))
    print("Claims table is visible")

    claim_forms_elements = driver.find_elements(By.XPATH, claim_forms)

    for claim in claim_forms_elements:
    
        claim_data_json = {}
        try:
            link_name = claim.text
            print(f"Clicking on first claim : {link_name}" )
            
            claim.click()
            
            claim_header = f'//h1[contains(text(),"Creditor Data Details - Claim # {link_name}")]'
            wait.until(EC.visibility_of_element_located((By.XPATH, claim_header)))
            cred_data_details_header_ele = driver.find_element(By.XPATH,claim_header)
    
            if cred_data_details_header_ele:
                print(f'Page opened for claim : {link_name}')
                
            print("Printing claim general details:")
    
            # Creditor address
            print("Creditor Span Address :")
            creditor_address_els = driver.find_elements(By.XPATH, main_address)
            if len(creditor_address_els) >0:
                creditor_address = driver.find_element(By.XPATH, main_address).text
                print(creditor_address)
                claim_data_json['creditor_address']=creditor_address
        
            # Debtor name
            print("Debtor name :")
            debtor_name_data_els = driver.find_elements(By.XPATH, debtor_name_data)
            if len(debtor_name_data_els) >0:
                debtor_name = driver.find_element(By.XPATH, debtor_name_data).text
                print(debtor_name)
                claim_data_json['debtor_name_data'] = debtor_name
                
            # Date filed
            print("Date filed :")
            date_filed_data_els = driver.find_elements(By.XPATH, date_filed_data)
            if len(date_filed_data_els) >0:
                original_date_filed = driver.find_element(By.XPATH, date_filed_data).text
                print(original_date_filed)
                claim_data_json['original_date_filed'] = original_date_filed
    
            # Claim number
            print("Claim number:")
            claim_number_data_els = driver.find_elements(By.XPATH, claim_number_data)
            if len(claim_number_data_els) >0:
                original_claim_number = driver.find_element(By.XPATH, claim_number_data).text
                print(original_claim_number)
                claim_data_json['original_claim_number'] = original_claim_number
        
            # Claim Date
            print("Claim Date:")
            schedule_number_data_els = driver.find_elements(By.XPATH, schedule_number_data)
            if len(schedule_number_data_els) >0:
                claim_date = driver.find_element(By.XPATH, schedule_number_data).text
                print(claim_date)
                claim_data_json['claim_date'] = claim_date
                
                
            # Claimed amount
            print("Claimed amount:")
            claimed_amount_els = driver.find_elements(By.XPATH, claimed)
            if len(claimed_amount_els) >0:
                claimed_amount = driver.find_element(By.XPATH, claimed).text
                print(claimed_amount)
                claim_data_json['claimed_amount'] = claimed_amount
    
            # Original history Claim Date
            print("History Claim Date:")
            hist_claim_date_els = driver.find_elements(By.XPATH, history_claim_date)
            if len(hist_claim_date_els) >0:
                original_history_claim_date = driver.find_element(By.XPATH, history_claim_date).text
                print(original_history_claim_date)
                claim_data_json['original_history_claim_date'] = original_history_claim_date
                
            # Original history Claim Text and Link
            print("History Claim Text:")
            hist_claim_text_els = driver.find_elements(By.XPATH, history_claim_text)
            if len(hist_claim_text_els) >0:
                original_history_claim_text = driver.find_element(By.XPATH, history_claim_text).text
                print(original_history_claim_text)
                claim_data_json['original_history_claim_text'] = original_history_claim_text
                original_history_claim_link = driver.find_element(By.XPATH, history_claim_href).get_attribute('href')
                print(original_history_claim_link)
                claim_data_json['original_history_claim_link'] = original_history_claim_link
                
            # Withdrawal history Docket Number
            print("Docket Number:")
            docket_no_els = driver.find_elements(By.XPATH, history_docket_number)
            if len(docket_no_els) >0:
                docket_no = driver.find_element(By.XPATH, history_docket_number).text
                print(docket_no)
                claim_data_json['docket_no'] = docket_no
    
            driver.find_element(By.XPATH,close_button).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, claim_column)))
            
            
            # # Objection Motion Date
            # print("Objection Motion date:")
            # obj_motion_date_els = driver.find_elements(By.XPATH, obj_date)
            # if len(obj_motion_date_els) >0:
            #     obj_motion_date = obj_motion_date_els[0].text
            #     print(obj_motion_date)
            #     claim_data_json['obj_motion_date'] = obj_motion_date
                
            # # Object Motion Text and Link
            # print("Object Motion Text:")
            # obj_motion_text_els = driver.find_elements(By.XPATH, obj_motion_text)
            # if len(obj_motion_text_els) >0:
            #     obj_motion_text = driver.find_element(By.XPATH, obj_motion_text).text
            #     print(obj_motion_text)
            #     claim_data_json['obj_motion_text'] = obj_motion_text
            #     obj_motion_link = driver.find_element(By.XPATH, obj_motion_href).get_attribute('href')
            #     print(obj_motion_link)
            #     claim_data_json['obj_motion_link'] = obj_motion_link
                
            # # Objection Order Date
            # print("Objection Order date:")
            # obj_order_date = obj_motion_date_els[1].text
            # print(obj_order_date)
            # claim_data_json['obj_order_date'] = obj_order_date
                
            # # Object Order Text and Link
            # print("Object Order Text:")
            # obj_order_text_els = driver.find_elements(By.XPATH, obj_order_text)
            # if len(obj_order_text_els) >0:
            #     obj_order_text = driver.find_element(By.XPATH, obj_order_text).text
            #     print(obj_order_text)
            #     claim_data_json['obj_order_text'] = obj_order_text
            #     obj_order_link = driver.find_element(By.XPATH, obj_order_href).get_attribute('href')
            #     print(obj_order_link)
            #     claim_data_json['obj_order_link'] = obj_order_link
                
            
            # # Object history basis
            # print("Object history basis:")
            # obj_hist_basis_els = driver.find_elements(By.XPATH, obj_hist_basis)
            # if len(obj_hist_basis_els) >0:
            #     obj_history_basis = driver.find_element(By.XPATH, obj_hist_basis).text
            #     print(obj_history_basis)
            #     claim_data_json['obj_history_basis'] = obj_history_basis
                
            # # Object history status
            # print("Object history status:")
            # obj_hist_status_els = driver.find_elements(By.XPATH, obj_hist_status)
            # if len(obj_hist_status_els) >0:
            #     obj_history_status = driver.find_element(By.XPATH, obj_hist_status).text
            #     print(obj_history_status)
            #     claim_data_json['obj_history_status'] = obj_history_status
                
            # json_data = json.dumps(claim_data_json)
            # main_json_data[f'{link_name}'] = json_data
            
        except Exception as e:
            #continue
            print(e)
                                              
        
    # Click next button
    wait.until(EC.visibility_of_element_located((By.XPATH, next_button)))
    next_buttons = driver.find_elements(By.XPATH,next_button)
    actions = ActionChains(driver)
    actions.move_to_element(next_buttons[1]).perform()
    next_buttons[1].click()
    
    wait.until(EC.visibility_of_element_located((By.XPATH, claim_column)))
    
    # Check current page
    current_page = driver.find_elements(By.XPATH,'//*[@id="pagenum"]')
    

    
    
with open('data.json', "w") as outfile:
    json.dump(main_json_data, outfile)