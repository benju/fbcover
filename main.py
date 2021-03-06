#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
import os
import cgi
import datetime
import webapp2
from bs4 import BeautifulSoup
import logging
from google.appengine.ext import db
#from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

from PIL import Image
from PIL import ImageEnhance
import cStringIO
import StringIO
import urllib2
import re
#class Greeting(db.Model):
#  author = db.UserProperty()
#  content = db.StringProperty(multiline=True)
#  date = db.DateTimeProperty(auto_now_add=True)

blob = "" 
size = (0,0)
logging.info("pic bc : " + blob[:10])

class MainPage(webapp2.RequestHandler):
  def get(self):
#    self.response.headers['Content-Type'] = "image/jpeg"
#    file = urllib2.urlopen("http://joelevis.files.wordpress.com/2012/06/fxcam_1339866304030.jpg")
#    im = cStringIO.StringIO(file.read())
#    image = Image.open(im)
#    out = StringIO.StringIO()
#    image.save(out, "JPEG") 
#    contents = out.getvalue()
#    self.response.out.write(contents)
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    template_values = {}
    self.response.out.write(template.render(path, template_values))

class ImageSh(webapp2.RequestHandler):
  def post(self):
    
    picture = self.request.get("img")
    global blob
    blob = picture 
#    logging.info("after ad : " +blob[:10])
#    self.response.out.write('<img src="/image"></img>') 
    path = os.path.join(os.path.dirname(__file__), 'templates/crop.html')
    template_values = {}
    self.response.out.write(template.render(path, template_values))

 

#logging.info("after ad outside class:" +pic.getvalue()[:10])

#class Fboutput(webapp2.RequestHandler):
#  def get(self):
#    status=1
#    fblink = str(self.request.get('link'))
#    conn = urlfetch.fetch(fblink)
#    if conn.status_code == 200: 
#      html = conn.content
#      soup = BeautifulSoup(html)
#      code = soup.find('code')
#    #Let the hacking begin....
#      string = str(code)
#      hackedhtml = re.sub('<!--', ' ', string)
#      soup = BeautifulSoup(hackedhtml)
#      url = soup.find('img')
#      if(url == None):
#        global status
#        status = 1
#      if(status==1):
#        try:
#          coverurl = url.attrs['src'] 
#        except:
#         status=0
#        if(status=1): 
#          fil=urllib2.urlopen(coverurl)
#          im = cStringIO.StringIO(fil.read())
#          userpic = Image.open(im)
#          bright = ImageEnhance.Brightness(userpic).enhance(1.5)
#          colored = ImageEnhance.Color(bright).enhance(0.4)
#          blurred = ImageEnhance.Sharpness(colored).enhance(-0.5)
#          path = os.path.join(os.path.dirname(__file__), 'transparent.png')
#          #file2 = urllib2.urlopen("http://joelevis.files.wordpress.com/2012/07/transparent.png")
#          #img = cStringIO.StringIO(file2.read())
#          poster = Image.open(path)
#          blurred.paste(poster, (0,0), poster )
#          out = StringIO.StringIO()
#          blurred.save(out, "JPEG")
#          contents = out.getvalue()
#          out.close()
#          self.response.headers['Content-Type']="image/jpeg"
#          self.response.out.write(contents)
#      else:
#        template_values = {}
#        path = os.path.join(os.path.dirname(__file__), 'templates/geterror.html')
#        self.response.out.write(template.render(path, template_values)) 

#    else:
#      template_values = {}
#      path = os.path.join(os.path.dirname(__file__), 'templates/linkerror.html')
#      self.response.out.write(template.render(path, template_values)) 

class DisplayHandler(webapp2.RequestHandler):
  def get(self):  
    global blob
    global size
    logging.info("inside anothet after ad : " +blob[:10])
#    logging.info("conv after ad " +picture.getvalue()[:10])
    tmp = Image.open(cStringIO.StringIO(blob))
    tmp.thumbnail((1024, 768), Image.ANTIALIAS)  
    blob = tmp.tostring()
    size = tmp.size
    out = StringIO.StringIO()
    tmp.save(out, "JPEG")
    contents = out.getvalue()
    out.close()
    self.response.headers['Content-Type'] = "image/jpeg"
    self.response.out.write(contents)       

class Imoutput(webapp2.RequestHandler):
  def post(self):
    global size
    x1 = int(float(self.request.get('x1'))) 
    y1 = int(float(self.request.get('y1'))) 
    x2 = int(float(self.request.get('x2'))) 
    y2 = int(float(self.request.get('y2')))   
#    im = Image.open(cStringIO.StringIO(blob))
    im = Image.fromstring('RGB',size, blob) 
    logging.info(x1)
    logging.info(y1)
    logging.info(x2)
    logging.info(y2)
    imag = im.crop((x1, y1, x2, y2))
    imag = imag.resize((425, 315))
    bright = ImageEnhance.Brightness(imag).enhance(1.5)
    colored = ImageEnhance.Color(bright).enhance(0.4)
    blurred = ImageEnhance.Sharpness(colored).enhance(-0.5)
    path = os.path.join(os.path.dirname(__file__), 'transparent.png')
    poster = Image.open(path)
    newim = Image.new('RGB', (851, 315), (255, 255, 255))
    newim.paste(blurred, (426, 0))
    newim.paste(poster, (0,0), poster)
    out = StringIO.StringIO()
    newim.save(out, "JPEG")
    contents = out.getvalue()
    out.close()
    self.response.headers['Content-Type']="image/jpeg"
    self.response.out.write(contents)

app = webapp2.WSGIApplication([
  ('/', MainPage),
#  ('/fb', Fboutput),
  ('/img', ImageSh),
  ('/image', DisplayHandler),
  ('/generate', Imoutput)
], debug=True)
