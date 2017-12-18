from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import argparse
import time
import pandas as pd

def get_args():
        parser = argparse.ArgumentParser(prog="kusis_control")
        parser.add_argument("--assignment", default='SpecifyAnAssignment', help="assignment")
        parser.add_argument("--user", default='', help="user name")
        parser.add_argument("--pass", default='', help="password")
        parser.add_argument("--grades", default='../data/ps10_withid.csv', help="the csv file that contains grade with ids")

        args = vars(parser.parse_args())
        return args

def find_assignment(browser, assignment):
    found = False
    index = -1
    try:
    
        while not found:
            boxblue = browser.find_element_by_id('ACE_DERIVED_LAM_')
            els = boxblue.find_elements_by_xpath('.//tr')
            for el in els:
                cols = el.text.encode('utf-8').strip().split()
                if assignment in cols:
                    found = True
                    index = cols.index(assignment)
                    break
            
            if not found:
                next_btn = browser.find_element_by_id('DERIVED_LAM_RIGHT_MOVE')
                next_btn.click()
                time.sleep(2)
    
    except Exception as e:
        print e

    return index

def enter_grades_to_boxes(browser, colindex, grades):
    total = 0
    student = 0

    while total == 0 or student != total:        
        el8 = browser.find_element_by_id('ACE_DERIVED_SSTSNAV_')
        tables = el8.find_elements_by_xpath(".//table[@role='presentation']")
        t = tables[4]
        trs = t.find_elements_by_xpath(".//tr")
        trs1 = trs[2::4]
        trs2 = trs[1::4]

        if total == 0:
            total = len(trs1)

        ntr = trs1[student]
        inptr = trs2[student]

        student += 1
        kusisid = ntr.text.encode('utf-8').strip().split()[-1]
        inps = inptr.find_elements_by_xpath(".//input[starts-with(@name, 'DERIVED_LAM_GRADE')]")
        box = inps[colindex]
        if box.is_enabled():
            print 'Kusis id: ', kusisid,
            q = grades.query('id == "{}"'.format(kusisid))
            if len(q) > 0:
                grade = q.get_values()[0, 2]
                print 'Grade: ', grade
                box.send_keys(str(grade))
                box.send_keys(Keys.ENTER)
                time.sleep(4)

def enter_grade(args):
    browser = webdriver.Chrome()
    browser.implicitly_wait(30)
    browser.get('https://kusis.ku.edu.tr')
    el = browser.find_element_by_id('login__username')
    el.send_keys(args['user'])
    el2 = browser.find_element_by_id('login__password')
    el2.send_keys(args['pass'])
    el2.submit()
    el3 = browser.find_element_by_id('pthnavbca_PORTAL_ROOT_OBJECT')
    el3.click()
    el4 = browser.find_element_by_id('fldra_CO_EMPLOYEE_SELF_SERVICE')
    el4.click()
    el5 = browser.find_element_by_id('fldra_HC_SS_FACULTY_CTR_GBL')
    el5.click()
    el6 = browser.find_element_by_id('crefli_HC_LAM_CLASS_GRADE_GBL')
    el6.click()
    browser.switch_to_frame('ptifrmtgtframe')

    index = find_assignment(browser, args['assignment'])
    
    if index == -1:
        print 'Assignment could not found...'
    else:
        grades = pd.read_csv(args['grades'])
        colindex = index - 2
        enter_grades_to_boxes(browser, colindex, grades)
        time.sleep(180)
    
    browser.quit()

if __name__ == "__main__":
    args = get_args()
    enter_grade(args)
