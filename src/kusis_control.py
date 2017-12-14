from selenium import webdriver
import argparse
import time

def get_args():
        parser = argparse.ArgumentParser(prog="kusis_control")
        parser.add_argument("--assignment", default='SpecifyAnAssignment', help="assignment")
        parser.add_argument("--user", default='', help="user name")
        parser.add_argument("--pass", default='', help="password")

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
                print 'Cols: ', cols
                if assignment in cols:
                    found = True
                    index = cols.index(assignment)
                    break
            
            if not found:
                next_btn = browser.find_element_by_id('DERIVED_LAM_RIGHT_MOVE')
                next_btn.click()
                time.sleep(3)
    
    except Exception as e:
        print e

    return index

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
        el8 = browser.find_element_by_id('ACE_DERIVED_SSTSNAV_')
        #print 'Table text: ', el8.text.encode('utf-8')
        trs = el8.find_elements_by_xpath('.//tr')
        
        for tr in trs:
            boxes = tr.find_elements_by_class_name('PSEDITBOX')
            print "Len boxes: ", len(boxes)

            for box in boxes:
                print box.text.encode('utf-8')

    browser.quit()

if __name__ == "__main__":
    args = get_args()
    enter_grade(args)
