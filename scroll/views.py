from flask import render_template,jsonify,json,session,redirect,url_for,request,current_app,make_response

from scroll import app

import requests
import re

from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def scroll():
    debug = None
    if request.method == 'POST':
        page_not_found(404)
    else:
        ## Default page display GET
        r = requests.get('http://services.realestate.com.au/services/listings/search?query={"channel":"buy","pageSize":"20"}').json()

        results_list = r['tieredResults'][0]['results']
        mainImage = []
        images = []
        link = []
        title = []
        address = []

        for i,item in enumerate(results_list):
            tmpStr = results_list[i]['mainImage']['server']+'/440x320'+results_list[i]['mainImage']['uri']+' '
            mainImage.append(tmpStr)
            images.append(results_list[i]['images'])
            link.append(results_list[i]['_links']['short'])
            title.append(results_list[i]['title'])
            address.append(results_list[i]['address'])

        app.logger.debug(link)
        #app.logger.debug(address)
        #app.logger.debug("complete...")
        return render_template('index.html',main_image=mainImage,images=images,link=link,title=title,address=address,debug=debug)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
