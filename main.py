from TemplateMatcher import TemplateMatcher

tm = TemplateMatcher("./img/eye.jpg")
tm.exec("./img/original.jpg", "TM_CCOEFF")
