"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
import pre  # Preprocess schedule file


###
# Globals
###
app = flask.Flask(__name__)
schedule = "static/schedule.txt"  # This should be configurable
import CONFIG


import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/schedule")
def index():
  app.logger.debug("Main page entry")
  raw = open('static/schedule.txt')
  processed = pre.process(raw)
 
  if 'schedule' not in flask.session:
      app.logger.debug("Processing raw schedule file")
      flask.session['schedule'] = processed[0]


  date=[]
  thisWeek =arrow.now().week
  for index in range(len(processed[0])):
    w = processed[1].replace(weeks=+index)
    if(w.week == arrow.now().week):
      nownindex = index
    date.append(w)

  return flask.render_template('syllabus.html', date=date)


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404

#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'currentweek' )
def is_current_week( i ):
    ithweek = pre.process(open('static/schedule.txt'))[1].week + i;
    return 'currentweek' if ithweek == arrow.now().week+1 else ''


#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
