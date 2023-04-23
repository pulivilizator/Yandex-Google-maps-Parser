from selenium import webdriver as wb_noproxy
def options():
	opt = wb_noproxy.ChromeOptions()
	opt.add_argument('--start-maximized')
	return opt