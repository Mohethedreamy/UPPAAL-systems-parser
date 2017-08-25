import xml.etree.ElementTree as ET
from tkinter import *
try:
    # for Python2
	from Tkinter import *
	import Tkinter, Tkconstants, tkFileDialog
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import filedialog


templates = []

root = Tk()
root.geometry("600x250")
canvasFrame = Frame(root,height=250, width=250)
canvas = Canvas(canvasFrame)
canvas_objs = [()]
lb = Listbox(root, selectmode=BROWSE)
old = 0


stats = ([])
trans = ([])

def init():
	temp = templates[0]
	# lb.bind("<<ListboxSelect>>", listClick)
	for item in templates:
		name = item.find('name')
		if name==None:
			name = 'unnamed'
		lb.insert(END, name.text)
	lb.activate(0)

	show(0)
	poll()

def poll():
	global old
	selected = lb.curselection()
	if selected != ():
		now = selected[0]
		if now != old:
			listClick(now)
			old = now
	root.after(250, poll)

def show(choice):
	global canvas
	canvas.destroy()
	canvas = Canvas(canvasFrame)
	canvas.pack()

	temp = templates[choice]
	parcour(temp)
	canvas.configure(scrollregion=canvas.bbox("all"))


def listClick(index):
	show(index)

def empty_canvas():
	global canvas_objs
	for obj in canvas_objs:
		canvas.delete(obj)
	canvas_objs = [()]

def create_circle(x,y):
	global canvas_objs
	print('circle')
	obj =canvas.create_oval(x,y, x+45, y+45, width=2, fill='white')
	canvas_objs.append(obj)
	return

def create_arrow(x1,y1,x2,y2,element):
	global canvas_objs
	print('arrow')
	nail = element.find('nail')
	if nail != None:
		x3 = nail.get('x')
		y3 = nail.get('y')
		x3 = int(x3)
		y3 = int(y3)
		if x2>x3:
			line = canvas.create_line(x1+22.5,y1+22.5, x3, y3+23, x2+22.5+22.5, y2+22.5, arrow="last" ,width=2)
			canvas.tag_lower(line)
		else:
			line =canvas.create_line(x1+22.5,y1+22.5,x3,y3+23, x2+22.5-22.5, y2+22.5, arrow="last" ,width=2)
			canvas.tag_lower(line)
		canvas_objs.append(line)	
		return
	if x1>x2:
		line = canvas.create_line(x1+22.5,y1+22.5, x2+22.5+22.5, y2+22.5, arrow="last" ,width=2)
		canvas.tag_lower(line)
	else:
		line =canvas.create_line(x1+22.5,y1+22.5, x2+22.5-22.5, y2+22.5, arrow="last" ,width=2)
		canvas.tag_lower(line)
	canvas_objs.append(line)
	return

def setStat(element):
	stats.append(element)
	idd = element.get('id')
	x = element.get('x')
	y = element.get('y')
	x = int(x)
	y = int(y)
	element_name = element.find('name')
	if element_name!=None:
		name = element_name.text
		name_x = element_name.get('x')
		name_y = element_name.get('y')
		name_x = int(name_x)
		name_y = int(name_y)
		print(name_x+name_y)
		setText(name,x,y)
		print("Location: ",idd,x,y, name, name_x, name_y)
	else:
		print(idd,x,y)

	create_circle(x,y)
	return

def setTransition(element):
	trans.append(element)
	source = element.find('source')
	target = element.find('target')
	if source != None and target!=None:
		source_id = source.get('ref')
		target_id = target.get('ref')
		print("transition: ", source_id, target_id)
		source_stat = findStat(source_id)
		target_stat = findStat(target_id)
		print(source_stat.tag, source_stat.attrib)
		print(target_stat.tag, target_stat.attrib)
		if source_stat != None and target_stat!=None:
			y1 = source_stat.get('y')
			x1 = source_stat.get('x')
			y2 = target_stat.get('y')
			x2 = target_stat.get('x')
			print(y2,x2)
			y1 = int(y1)
			x1 = int(x1)
			y2 = int(y2)
			x2 = int(x2)
			create_arrow(x1,y1,x2,y2,element)
			# labels
			for sub in element:
				if sub.tag == 'label':
					y = sub.get('y')
					x = sub.get('x')
					x = int(x)
					y = int(y)
					label_text = sub.text
					setTextL(label_text,x + 25,y + 35)
	return

def setText( str,x,y):
	global canvas_objs
	print('text')
	txt = canvas.create_text(x+25,y-10,text=str)
	canvas_objs.append(txt)
	canvas.tag_raise(txt)

def setTextL( str,x,y):
	global canvas_objs
	print('text')
	txt = canvas.create_text(x+25,y-10,text=str,anchor=NW)
	canvas_objs.append(txt)
	canvas.tag_raise(txt)	

def parcour(temp):
	for element in temp:
		if element.tag == 'location':
			setStat(element)
		if element.tag == 'transition':
			setTransition(element)
	canvas.configure(scrollregion=canvas.bbox("all"))

def findStat(idd):
	for stat in stats:
		if stat.get('id')==idd:
			return stat

	return None

def OpenNet():
	global templates
	lb.delete(0,END)
	try:
		filename =tkFileDialog.askopenfilename(filetypes = (("xml files","*.xml"),("all files","*.*")))
	except:
		filename =filedialog.askopenfilename(filetypes = (("xml files","*.xml"),("all files","*.*")))
	print ("Opening: ",filename)
	tree = ET.parse(filename)
	node = tree.getroot()
	templates = node.findall('template')
	init()




#init()
# canvas.configure(scrollregion=canvas.bbox("all"))
canvas.pack()
OpenBtn = Button(root, text="Open file", command=OpenNet, width=10)
OpenBtn.pack(side=BOTTOM)
canvasFrame.place(x=150,y=20)
lb.place(x=10, y=10)
root.mainloop()
