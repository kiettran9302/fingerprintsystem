


# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

class SSD1306:
	def __init__(self):
		# Raspberry Pi pin configuration:
		self.RST = None     # on the PiOLED this pin isnt used
		# Note the following are only used with SPI:
		self.DC = 23
		self.SPI_PORT = 0
		self.SPI_DEVICE = 0
		self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.RST)
		# Initialize library.
		self.disp.begin()

		#Clear display.
		self.disp.clear()
		self.disp.display()
		# Create blank image for drawing.
		# Make sure to create image with mode '1' for 1-bit color.
		self.width = self.disp.width
		self.height = self.disp.height
		self.image = Image.new('1', (self.width, self.height))

		# Get drawing object to draw on image.
		self.draw = ImageDraw.Draw(self.image)

		# Draw a black filled box to clear the image.
		self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

		# Draw some shapes.
		# First define some constants to allow easy resizing of shapes.
		self.padding = -2
		self.top = self.padding
		self.bottom = self.height-self.padding
		# Move left to right keeping track of the current x position for drawing shapes.
		self.x = 0


		# Load default font.
		self.font = ImageFont.truetype('./Bebas-Regular.ttf', 12)
		

