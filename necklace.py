from scikits.audiolab import wavread
import math
import svgwrite
import xml.etree.ElementTree as etree
from flask import Flask, render_template, request, redirect, send_file
from werkzeug import secure_filename
import os, os.path
from StringIO import StringIO
from urllib import urlencode

app = Flask(__name__)
upload_path = os.environ.get("UPLOAD_PATH", "/tmp")

gap = 5.0
inner = 1.25
width = 181

minD = 5
step = 1.5
maxD = 21.5

@app.route('/')
def index():
    return render_template('index.html')

def ringEncode(filename, rings):
	return "filename=%s&"%filename + urlencode([("ring", r) for r in rings])

@app.route('/upload-audio', methods=['POST'])
def upload():
	ringCount = int(request.form["samples"])
	file = request.files['audio']
	if file.filename == "":
		return redirect("/")
	filename = secure_filename(file.filename)
	fullpath = os.path.join(upload_path, filename)
	file.save(fullpath)
	try:
		rings = createRings(fullpath, ringCount)
		return redirect("/rings?" + ringEncode(filename, rings))
	except IOError, e:
		print e
		return redirect("https://http.cat/415") # unsupported media type
	finally:
		os.unlink(fullpath)

@app.route('/rings')
def ringsPage():
	rings = [int(x) for x in request.args.getlist("ring")]
	filename = request.args["filename"]
	steps = max(rings)
	counts = [sum([1 for r in rings if r == x]) for x in range(1, steps+1)]
	return render_template("rings.html",
		rings = rings,
		filename = filename,
		counts = counts,
		svgQuery = ringEncode(filename, rings),
		steps = steps,
		step = step,
		minD = minD
	)

@app.route('/create-svg')
def createSVG():
	rings = [int(x) for x in request.args.getlist("ring")]
	filename = request.args["filename"]
	xml = StringIO(createNecklace(rings))
	fname = filename + ".svg"
	return send_file(xml, as_attachment = True, attachment_filename = fname)

def createRings(filename, samples):
	data, fs, enc = wavread(filename)
	if data.ndim == 1: # mono
		maxValues = data
	else: # stereo
		maxValues = data.max(axis = 1)
	perRing = len(data)/samples
	steps = int((maxD - minD)/step) + 1
	highest = [maxValues[(perRing*i):(perRing*(i+1))].max() for i in range(samples)]
	biggest = max(highest)
	perStep = biggest/steps
	return [int(math.ceil(x/perStep)) for x in highest]

def createNecklace(rings):
	dwg = svgwrite.Drawing(size = ("181mm", "181mm"))

	location = [5,5]
	blue = "rgb(0,0,255)"
	format = "%.2fmm"

	for ring in rings:
		diameter = (ring-1)*step + minD

		if location[0] + diameter > width:
			location[0] = 5
			location[1] += maxD + gap

		radius = diameter / 2.0
		dwg.add(dwg.circle(center = (format%(location[0] + radius), format%(location[1] + radius)),
	                                   r = format %radius ,
	                                   stroke_width = "0.01mm",
	                                   stroke = blue,
	                                   fill = "none"))
		dwg.add(dwg.circle(center = (format%(location[0] + radius), format%(location[1] + radius)),
	                                   r = format % inner,
	                                   stroke_width = "0.01mm",
	                                   stroke = blue,
	                                   fill = "none"))

		location[0] += diameter + gap

	# http://stackoverflow.com/a/4590052/320546
	def indent(elem, level=0):
	    i = "\n" + level*"\t"
	    if len(elem):
	        if not elem.text or not elem.text.strip():
	            elem.text = i + "\t"
	        if not elem.tail or not elem.tail.strip():
	            elem.tail = i
	        for elem in elem:
	            indent(elem, level+1)
	        if not elem.tail or not elem.tail.strip():
	            elem.tail = i
	    else:
	        if level and (not elem.tail or not elem.tail.strip()):
	            elem.tail = i

	root = dwg.get_xml()
	indent(root)
	return etree.tostring(root)

if __name__ == "__main__":
	app.run(debug=True)
