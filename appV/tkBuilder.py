import tkinter as tk
from tkinter import messagebox
import xml.dom.minidom
import cssutils
import inspect

# --------------------------------------------------- CUSTOM WIDGETS -------------------------------------------------#
class Graph(tk.Canvas):
	def __init__(self,root, **kw):
		super().__init__(root, width=kw.get('width'), height=kw.get('height'), bg=kw.get('bg'))
		self.fill = kw.get('fill')
		self.width = int(kw.get('width')) if kw.get('width') else 30
		self.height = int(kw.get('height')) if kw.get('height') else 100
		self.bar = self.create_rectangle(0,self.height,self.width,self.height*2, tag='rect', fill=self.fill, outline=self.fill)
		self.setValue(int(kw.get('value')) if kw.get('value') else 1)

	def setValue(self,value):
		y = self.coords(self.bar)[1]
		self.move(self.bar, 0, self.height - self.height * value - y)


# -------------------------------------------------------- BUILDER ---------------------------------------------------#
class Builder(tk.Frame):
	def __init__(self, appPath, stylePath=None):
		self.widgets = {}
		self.functions = {'pass':self.pass_}
		self.tree = xml.dom.minidom.parse(appPath)
		if stylePath:
			self.style = self.getStyle(stylePath)
			self.applyStyle(self.tree)

		self.master = tk.Tk()
		super().__init__(self.master)
		
		self.master.title(self.tree.getElementsByTagName('app')[0].getAttribute('title'))
		self.pack()
	
	def getStyle(self, stylePath):
		sheet = cssutils.parseFile(stylePath)
		styleMethods = {}
		for item in sheet:
			if item.type == item.STYLE_RULE:
				attrs = {}
				for property in item.style:
					attrs[property.name] = property.value
				styleMethods[item.selectorText] = attrs
		return styleMethods
	
	def applyStyle(self, root):
		for element in root.childNodes:
			# case it's a text object
			if type(element) == xml.dom.minidom.Text:
				continue

			if (elementStyle := self.style.get(element.tagName)) or (elementStyle := self.style.get(f'#{element.getAttribute("id")}')) or (elementStyle := self.style.get(f'.{element.getAttribute("class")}')):
				[element.setAttribute(*item) for item in elementStyle.items()]
			
			if element.childNodes != []:
				self.applyStyle(element)


	def build(self):
		for frame in self.tree.getElementsByTagName('frame'):
			if frame.getAttribute('type') == 'pack' or not frame.getAttribute('type'):
				self.__pack__(frame)
			elif frame.getAttribute('type') == 'grid':
				self.__grid__(frame)
			else:
				print(f'unvalid frame type {frame.getAttribute("type")}')
		
		#for each frame, build every widgets using the self.__functions__() methods
		
	def __getSide__(self, side):
		if side == 'top':
			return tk.TOP
		if side == 'bottom':
			return tk.BOTTOM
		if side == 'left':
			return tk.LEFT
		if side == 'right':
			return tk.RIGHT
		return None

	# ---------------------------------------------- WIDGETS BUILDER -------------------------------------------------#
	def __grid__(self, frameTree):
		# get attributes of the widget
		attrs = dict()									
		for attr in dict(frameTree.attributes).keys():
			if(attr not in ['id','pos','command','default','type']):
				attrs[attr] = frameTree.getAttribute(attr)
		frame = tk.Frame(self.master, **attrs)

		for i, row in enumerate(frameTree.getElementsByTagName('row')):
			for j, element in enumerate(filter(lambda x : type(x) == xml.dom.minidom.Element, row.childNodes)):

				# get attributes of the widget
				attrs = dict()									
				for attr in dict(element.attributes).keys():
					if(attr not in ['id','pos','command','default']):
						attrs[attr] = element.getAttribute(attr)
				
				# assign funtcion if it exist
				if (f := element.getAttribute('command')) in self.functions:
					attrs['command'] = self.functions[f]

				# build widget based on type
				if element.tagName == 'label':
					v = ' '.join(t.nodeValue for t in element.childNodes)
					widget = tk.Label(frame, text=v, **attrs)

				elif element.tagName == 'entry':
					widget = tk.Entry(frame, **attrs)
					widget.insert(tk.END, element.getAttribute('default'))

				elif element.tagName == 'graph':
					widget = Graph(frame, **attrs)

				elif element.tagName == 'scale':
					widget = tk.Scale(frame, **attrs)

				else:
					continue
					# raise(f'unvalid widget type {element.tagName}')
				# add condition here if you want more widget types
				
				y = row.getAttribute('pos') if row.getAttribute('pos') else i
				x = element.getAttribute('pos') if element.getAttribute('pos') else j
				widget.grid(row=y, column=x)
				
				self.widgets[widgetId if (widgetId := element.getAttribute('id')) else len(self.widgets)] = widget

		frame.pack()

	def __pack__(self, frameTree):
		attrs = dict()									
		for attr in dict(frameTree.attributes).keys():
			if(attr not in ['id','pos','command','default','type']):
				attrs[attr] = frameTree.getAttribute(attr)
		frame = tk.Frame(self.master, **attrs)

		for i, element in enumerate(filter(lambda x : type(x) == xml.dom.minidom.Element, frameTree.childNodes)):
			# get attributes of the widget
			attrs = dict()									
			for attr in dict(element.attributes).keys():
				if(attr not in ['id','pos','command','default']):
					attrs[attr] = element.getAttribute(attr)
			
			# assign funtcion if it exist
			if (f := element.getAttribute('command')) in self.functions:
				attrs['command'] = self.functions[f]

			# build widget based on type
			if element.tagName == 'label':
				v = ' '.join(t.nodeValue for t in element.childNodes)
				widget = tk.Label(frame, text=v, **attrs)

			elif element.tagName == 'entry':
				widget = tk.Entry(frame, **attrs)
				widget.insert(tk.END, element.getAttribute('default'))

			elif element.tagName == 'graph':
				widget = Graph(frame, **attrs)

			elif element.tagName == 'scale':
				widget = tk.Scale(frame, **attrs)

			else:
				continue
				# raise(f'unvalid widget type {element.tagName}')
			# add condition here if you want more widget types

			side = self.__getSide__(element.getAttribute('pos'))
			widget.pack(side = side)

		frame.pack()

	# ---------------------------------------------- DEFAULT TRIGGERED FUNCTION --------------------------------------#
	def pass_(self, n):
		pass

	def test(self):
		print('test worked !')


# --------------------------------------------------------- SAMPLE ---------------------------------------------------#

if __name__ == '__main__':
	print('docs will be available soon !')
	app = Builder('default.xml', 'dark.css')
	app.build()
	app.mainloop()