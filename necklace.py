from scikits.audiolab import wavread
import sys, math
import svgwrite
import xml.etree.ElementTree as etree

samples = int(sys.argv[2])
data, fs, enc = wavread(sys.argv[1])
if data.ndim == 1: # mono
	maxValues = data
else: # stereo
	maxValues = data.max(axis = 1)
perRing = len(data)/samples

gap = 5.0
inner = 2.5
width = 181

minD = 5
step = 1.5
maxD = 21.5
steps = int((maxD - minD)/step) + 1
print steps

highest = [maxValues[(perRing*i):(perRing*(i+1))].max() for i in range(samples)]
print highest
biggest = max(highest)
perStep = biggest/steps
print perStep
rings = [int(math.ceil(x/perStep)) for x in highest]
print rings

rings = rings *2

counts = [sum([1 for r in rings if r == x]) for x in range(1, steps+1)]
print counts
for i in range(steps):
	toprint = "".join(["*" if x > i else " " for x in rings])
	print toprint

fname = sys.argv[1].replace("wav", "svg")
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
                                   r = format % (inner/2.0),
                                   stroke_width = "0.01mm",
                                   stroke = blue,
                                   fill = "none"))

	location[0] += diameter + gap

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
open(fname, "w").write(etree.tostring(root))