#!/usr/bin/python3

from flask import Flask,make_response,redirect,abort
from flask import render_template,request,jsonify
from flask.ext.bootstrap import Bootstrap

import requests,json,os
import auth
import log


app = Flask(__name__)
bootstrap = Bootstrap(app)

url = 'http://127.0.0.1:5120/iot/spi/'


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    log.logger.info("call : login()")
    if request.method == 'POST':
        log.logger.debug("login post method")
        username = request.form['username']
        password = request.form['password']

        if auth.authority_user(username,password):
            #return render_template('tenant.html')
            return redirect("/tenant")

        else:
            return jsonify('404.html')

    return render_template('login.html')


@app.route('/console',methods=['GET', 'POST'])
def console():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        print(username,password)



    return render_template('console.html')

@app.route('/site')
def site():
    res = requests.get(url + "sites").json()
    #log.logger.info(res)
    sites = res["result"]
    return render_template('site.html',sites=sites)

@app.route('/tenant')
def tenant():
    res = requests.get(url + "tenants").json()
    #log.logger.info(res)

    return render_template('tenant.html',tenants=res["result"])

@app.route('/device')
def device():
    res = requests.get(url + "devices?type=all").json()
    #log.logger.info(res)

    return render_template('device.html',devices = res["result"])

@app.route('/user/<name>',methods=['GET', 'POST'])
def get_user(name):

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['metadata']

        print(username,password)

    res = requests.get(url + "users").json()
    #print(res["result"])
    users = res["result"]

    return render_template('user.html', name=name,users = users)

@app.route('/logout')
def logout():
    return render_template('index.html')


# show photo
@app.route('/img/<string:filename>', methods=['GET'])
def img_handle(filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            log.logger.debug('filename is %s' % filename)
            image_data = open(os.path.join('./static/img', '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

#css
@app.route('/css/<string:filename>', methods=['GET'])
def css_handle(filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            log.logger.debug('filename is %s' % filename)
            image_data = open(os.path.join('./static/css', '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'text/css'
            return response
    else:
        pass

#js
@app.route('/js/<string:filename>', methods=['GET'])
def js_handle(filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            log.logger.debug('filename is %s' % filename)
            image_data = open(os.path.join('./templates/js', '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'text/javascript'
            return response
    else:
        pass



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=False)
    """
	from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
	"""
