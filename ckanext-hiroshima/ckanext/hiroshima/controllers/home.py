from ckan.controllers.home import HomeController
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import os
import glob

class HiroshimaHomeController(HomeController):
    # vuejs build file output destination
    DIST_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../public/dist"

    def usePolicy(self):
        return toolkit.render('home/usepolicy.html')

    def aboutUse(self):
        return toolkit.render('home/about-use.html')

    def opinion(self):
        return toolkit.render('home/opinion.html')

    def index(self):
        css_list = []
        js_list = []

        # Get css,js file name
        for css in glob.glob(self.DIST_DIRECTORY_PATH + "/css/*.css") :
            css_list.append(os.path.split(css)[1])

        for js in glob.glob(self.DIST_DIRECTORY_PATH + "/js/*.js") :
            js_list.append(os.path.split(js)[1])

        # Stored in template variable
        extra_vars = {
            "css_list" : css_list,
            "js_list" : js_list
        }

        return toolkit.render('home/index.html', extra_vars)
