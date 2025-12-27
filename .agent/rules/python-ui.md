---
trigger: always_on
---

UI layers

Layers are root "windows", their purpose to hold all kind of interface windows while managing the z order of the windows (z order = depth level of the windows, which one is "above" the other). By default there are 5 layers (from bottom to top):

"GAME": this is only used for the game window (game.py), and when you click on it the game will translate the click position to the map
"UI_BOTTOM": this is used for shop titles
"UI": this is the default layer, we would like to put most of our windows into this layer, like inventory, character window, messenger, pms, etc, so they can overlap each other
"TOP_MOST": every window, that should always be in front of the player, so other windows would not overlap them from the lower layers, so for example the taskbar is placed in this layer
"CURTAIN": this is for the curtain window, which is actually a black as a pit window, that is used to smooth the change from different introXX windows (like between login and charselect) This is the outest layer and goes before the other 4.
 

So when the render happens, the 1st layer and its childs will be rendered first, then the 2nd layer, then the 3rd, etc, so by this we will get our comfy usual client layout. In the other hand, when we click, everything goes in reverse order, first the client will try to "pick" from the curtain layer's child windows (also in reverse order), then the top_most layer, etc. Ofc there is no layers beyond the game layer, so usually the "pick" will succeed there, and we will end up clicking on the map.

 

UI windows

Now lets talk a little bit about the parts of an UI window. It has a python object part and a c++ object part. When you create a basic Window (from the ui.py) basically 2 things happen: a python Window object is created first, then through the wndMgr.Register call a c++ CWindow object is created. These 2 objects are linked, in python the handle for the CWindow is saved in the self.hWnd variable, while in the CWindow the python object handle would be stored in the m_poHandler.

 

What are these handles for? If you want to call a method on a window from python, you have to specify which window you want to perform that action on. Remember, the python part is just a "frontend" for the UI, the actual magic happens in the cpp part. Without python, its possible to create windows, but without the cpp part there is no windows at all. On the cpp part, we need the python object handle to perform callbacks, like notifying the python class when we press a key, or pressing our left mouse button.

By default the newly created window will take a seat in one of the layers (if provided through the register method, otherwise it goes to the UI layer). In a healthy client we only put useful windows directly into a layer. For example you want to put your brand new won exchange window into the UI layer, but you don't want to put all parts of a window into the UI layer (for example putting the base window into the root layer then putting the buttons on it to the root layer too, then somehow using global coordinates to make it work).

 

Instead, you want to "group" your objects, using the SetParent function. You may say that "yeah yeah who doesn't know this?", but do you know what actually happens in the background? The current window will be removed from its current parent's child list (which is almost never null, cus when you create it its in the UI layer, so the parent is the UI layer) and will be put into the end of the new parent window's child list.

Why is it important, that it will be put into the end? Because it will determine the Z order of the childs of the window. For example if I create 2 ImageBox with the same size of image on the same position and then I set ImageBox1's parent before ImageBox2's parent, then I will only see ImageBox2, because that will be rendered after ImageBox1, because its position in the childList is lower than ImageBox2's. For normal window elements (like buttons) its very important, because after you set the parent of a window, you can't alter the z order (or rather the position in the childList) unless you use the SetParent again. No, you can't use SetTop, because its only for windows with "float" flags on it, which you only want to use on the base of your window (the root window that you put your stuff on it and use it as parent for most of the time).

 

Window picking

"Picking" is performed when we move the cursor. This is an important method, because this will determine the result of various events, for example the OnMouseOverIn, OnMouseOverOut, OnMouseRightButtonDown, etc. To fully understand it, you must keep in mind that every window is a square.  Do you have a perfect circle image for a button? No you don't, its a square. Do you have the most abstract future window board design with full star wars going on the background? No, you DON'T. ITS A SQUARE. By default, a window is picked if:

the mouse is over the window AND
the window is visible (Shown) AND
the window doesn't have "not_pick" flag set AND
the window is "inside its parent's square" on the current mouse position, which means if the parent's position is 0,0 and it has a size of 10x10 and the window's position is 11, 0, the window is outside of its parent's square. This is really important to understand, lots of UI has fully bugged part because of ignoring this fact. I think every one of you already experienced it on some bad illumina design implementation, when you click on a picture, and your character will start to run around like a madman, because the game says that A-a-aaaaa! There is NO WINDOW ON THAT POSITION ;)
 

It is useful to use the not_pick flag whenever you can, for example on pure design elements, like lines and flowers and ofc the spaceships on the background. Lets say you have a size of 10x10 image that has a tooltip, and you have a window on it that has a size of 5x5. When the mouse is over the image, the tooltip will be shown, but if its over the 5x5 window, the tooltip won't appear, unless you set it to the 5x5 window too. But if you use the not_pick flag on the 5x5 window, the 5x5 window won't be picked and the tooltip would be shown even if the mouse is over the 5x5 window.

 

Window deletion, reference counting, garbage collector, proxying

The window deletion procedure starts on the python side, first the destructor of the python object will be called, then it will call the wndMgr.Destroy that deletes the c++ object. By default, we have to store our python object, or this time our python window, to make sour it doesn't vanish. Usually we do this via the interface module, like "self.wndRandomThing = myModule.RandomWindow()". But what is this? What is in the background?

Python objects has reference count. Let me present it with the following example:

a = ui.Window() # a new python object is created, and its reference count is 1
b = a # no new python object is created, but now b is refering to the same object as 'a', so that object has a refence count of 2
del b # b is no longer exists, so its no longer referencing to the newly created window object, so its reference count will be 1
del a # the newly created window object's reference count now 0, so it will be deleted, calling the __del__ method
To be more accurate, del-ing something doesn't mean that it will be deleted immediately. If the reference count hits 0 the garbage collector (btw there is garbage collector in python if you didn't know) will delete it, and that moment the __del__ will be called. It sounds very handy isn't it? Yeeeeah its easyyyy the coder don't have to manage object deletion its sooo simple.... Yeah... But lets do the following:

class stuff(object):
	def __del__(self):
		print "del"
	def doStuff(self):
		self.something = self.__del__ # here we could just simply do self.something = self too, doesnt matter

a = stuff()
a.doStuff() # and now you just cut your leg
del a #you are expecting the "del" print, but that will never happen
You may say " ? oh please who tf does something stupid like this? It SO OBVIOUS that its wrong whaaaaaaat????" But in reality, I could count on only one of my hand how many devs don't make this mistake. Even my codes from the past decade are bad according to this aspect, since I only realized this problem about a year ago, when I was working on the AE wiki. Even the yimir codes contain tons of this kind of errors, however there was definitely a smart man, who implemented the __mem_func__. Okay, I see that you still don't understand how is this possible to make this kind of mistake, so let me show you a real example:

class myBoard(ui.Board):
	def __init__(self):
		super(myBoard, self).__init__()
		self.makeItRain()
    
	def __del__(self):
		super(myBoard, self).__del__()
		print "I want to break free. I want to breeaaaaaak freeeeeeeeeeee"
    
	def doNothing(self):
		pass
  
	def makeItRain(self):
		self.btn = ui.Button()
		self.btn.SetParent(self)
		self.btn.SetEvent(self.doNothing) #boom

a = myBoard()
del a
# but where is the print?
Thats not that obvious now right? What happens here? We create a myBoard object, which in the __init__ calls to the makeItRain func, which stores an ui.Button object, and sets the button to call for the myBoard class's doNothing function with the self object pointer in the OnLeftMouseButtonDown function, which means that the reference count will never be zero, because the btn referenced in the myBoard but myBoard is referenced in the btn but the btn is referenced in the.... so you know, its a spiral of death, that our best friend garbage collector can't resolve.

 

Okay, but how to do it correctly? Lets talk about proxying. In python, proxies are weak references, which means that they don't increase reference count of an object, which is exactly what we need.

#let me show this time the console output too
class stuff(object):
	def __del__(self):
		print "del"

>>> from weakref import proxy
>>> a = stuff() #newly created object
>>> b = proxy(a) #create weak reference to the new object (note that the weak reference object is also an object that stores the weak reference)
>>> b #what is b?
<weakproxy at 02DB0F60 to stuff at 02DBFB50> # b is a weakproxy object that refers to a which is a "stuff object"
>>> del b # what if we delete b?
# no "del" message, the stuff object is not deleted, because its reference count is still 1, because its stored in a
>>> b = proxy(a) # lets recreate b
>>> del a # now we delete the only one reference of the stuff object
del # and here we go, we got the del message from __del__
>>> b # okay but whats up with b?
<weakproxy at 02DB0F60 to NoneType at 7C2DFB7C> # because b is a weakproxy object, it won't be deleted out of nowhere, but it refers to a NoneType right now, because the stuff object is deleted (also note here that NoneType is also a python object :D)
>>> if b: #what if I want to use b?
...     print "a"
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ReferenceError: weakly-referenced object no longer exists # in normal cases no need to trycatch this exception, because if we do everything right, we will never run into a deleted weakly-referenced object
But how do we proxy something like self.doNothing? Actually, what is self.doNothing? self.doNothing has 3 parts:

The first part is not that obvious, it has a base class pointer, which is points to myBoard.
It has a class object pointer, that is basically "self". It refers to the current instance of myBoard.
It has a function object pointer, called doNothing, which is located inside the myBoard class.
 

And now we can understand ymir's ui.__mem_func__ class, which is exactly meant to be used for proxying class member functions:

# allow me to reverse the order of the definitions inside the __mem_func__ so it will be more understandable
class __mem_func__:
	def __init__(self, mfunc): #this happens when we write ui.__mem_func__(self.doSomething)
		if mfunc.im_func.func_code.co_argcount>1: # if th