#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#	
#	mm3-keyboard.py tries to help you get your fonts and xkb data on
#	Linux/Unix system. It makes you easy install and remove.
#
#	copyright (c) 2009, Phone Htut <phonehtut2@gmail.com>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#	If that URL should fail, try contacting the author.

""" 	mm3-keyboard.py module
	This module tries to help you get your fonts and xkb data on
	Linux/Unix system.
"""
__author__ = "Phone Htut <phonehtut2@gmail.com>"
__copyright__ = "Copyright (c) 2009, Phone Htut"
__license__  = "GPLv3"


""" 	mm3-keyboard package """
__version__ = "0.1.1"
__metor__ = "box02 <thebox02@gmail.com>"

import glob
import re
import os
import subprocess
import sys

#Classifying operating system paths, you can add other distro fhs.
class Linux:
	fonts_dir = '/usr/share/fonts'
	doc_dir = '/usr/share/doc'
	xkb_dir = ['/usr/share/X11/xkb/symbols', '/etc/X11/xkb/symbols']
	def __init__(self):
		""" Classifying Linux FHS """
		print "Using Linux FHS...\n"

class FreeBSD:
	fonts_dir = '/usr/local/lib/X11/fonts'
	doc_dir = '/usr/local/share/doc'
	xkb_dir = '/usr/local/share/X11/xkb/symbols'
	def __init__(self):
		""" Classifying FreeBSD FHS """
		print "Using FreeBSD FHS...\n"


# Detecting distributions and finding correct paths for installation
if sys.platform.startswith('linux'):
	print '\nYour system is running Linux'
	use_fhs = Linux()
	possible_xkb_dirs = use_fhs.xkb_dir
	for correct_xkb_dir in possible_xkb_dirs:
		if os.path.exists(correct_xkb_dir):
			XKB_DIR = correct_xkb_dir
			break
	FONT_DIR = use_fhs.fonts_dir
	DOC_DIR = use_fhs.doc_dir
elif sys.platform.startswith('freebsd'):
	print '\nYour system is running FreeBSD'
	use_fhs = FreeBSD()
	FONT_DIR = use_fhs.fonts_dir
	DOC_DIR = use_fhs.doc_dir
	XKB_DIR= use_fhs.xkb_dir
else:
	sys.exit('Sorry, please try on Linux/Unix system!\n')

# Checking source paths and source files
print 'Checking source files from the package...'
"""	Checking source files in your package if you distribute
	In order to work with this module, you might need to put your fonts, 
 	xkb symbols file and other files in src_path named src folder, 
 	otherwise you might have to declare your src_path.
 	for example:
		src_path = './src0/' and './src1'
		font_file = './src0/?.ttf'
		xkb_data = './src0/mm'

"""
# my source folder and files here:
src_path_0 = './src0/'
xkb_data = 'mm'

# finding fonts
if os.path.exists(src_path_0):
	for src_font in os.listdir(src_path_0):
		if src_font.endswith('ttf'):
			# real working path
			src_font = os.path.join(src_path_0, src_font)
			# for show font only
			disp_src_font = src_font
			num_src_l = len(src_path_0)
			disp_src_font = disp_src_font[num_src_l:]
	 		print 'Font : %s [ OK ]' % disp_src_font
			break
else:
	print 'error: Font not found.'
	sys.exit("Interrupted installation.\n")
	
# finding mm files
src_xkb_data = os.path.join(src_path_0, xkb_data)
if os.path.exists(src_xkb_data):
	xkb_data = open(src_xkb_data).read()
	if xkb_data.find('mm3')== -1 and xkb_data.find('kuniyoshi@fastmail.fm')== -1:
		print 'error: You have NOT mm3 xkeyboard file!'
	else:
		print 'Xkeyboard : mm3 Keyboard [ OK ]\n'
else:
	print 'error: mm xkeyboard file not found.'
	sys.exit("Interrupted installation.\n")

# Installation fonts and keyboard data
def install():
	""" Install font and xkeyboard data """
	# making directories 
	print 'Installing directories...'
	new_font_dir = os.path.join(FONT_DIR, FONTNAME)
	new_doc_dir = os.path.join(DOC_DIR, FONTNAME)
	os.mkdir(new_font_dir)
	os.mkdir(new_doc_dir)
	print 'Installing directories done.'

	# installing font file
	print 'Installing %s font...' % FONTNAME
	if os.path.exists(new_font_dir):
		os.system('cp %s %s' % (src_font, new_font_dir))
		print 'Installing %s font done.' % FONTNAME
	else:
		print 'error: Font not installed!'
	
	# backing up existing mm file
	print 'Backuping original mm xkb file...'
	mm_orig = os.path.join(XKB_DIR, 'mm')
	os.rename(mm_orig, mm_orig + '_bak')
	mm_bak = os.path.join(XKB_DIR, 'mm_bak')
	if os.path.exists(mm_bak):
		print 'Backuping original mm xkb file done.'
	else:
		print 'error: Not backup original xkb file!'
		
	# install mm3 xkeyboard
	print 'Installing mm3 xkeyboard...'		
	os.system('cp %s %s' % (src_xkb_data, XKB_DIR))
	mm_new = os.path.join(XKB_DIR, 'mm')
	if os.path.exists(mm_new):
		print 'Installing %s keyboard done.' % FONTNAME
	else:
		print 'error: Not install xkeyboard!'
		
	# install documents
	print 'Installing documents...'
	os.system('cp AUTHORS changelog %s' % (new_doc_dir))
	os.system('cp COPYRIGHT CREDITS %s' % (new_doc_dir))
	print 'Installing documents done.'
	
# Removing fonts and keyboard data
def remove():
	""" Remove the installation files and data """
	# check and delete previous installed package 
	dest_font_dir = os.path.join(FONT_DIR, FONTNAME)
	dest_doc_dir = os.path.join(DOC_DIR, FONTNAME)
	
	if os.path.exists(dest_font_dir):
		print 'Removing previous installed %s font directory...' % FONTNAME
		os.system('rm -rf ' + dest_font_dir)
	if os.path.exists(dest_doc_dir):
		print 'Removing previous installed %s doc directory...' % FONTNAME
		os.system('rm -rf ' + dest_doc_dir)

	# restore origial or backup xkb_data file
	mm_backup = os.path.join(XKB_DIR, 'mm_bak')
	mm_original = os.path.join(XKB_DIR, 'mm')
	if os.path.exists(mm_backup):
		print 'Restoring mm backup file...'
		os.rename(mm_backup, mm_original)
		if os.path.exists(mm_original):
			print 'Restoring origianl or backup mm file done.'
		else:
			print 'error: Not restore from backup file!'
	else:
		print 'Skip Restoring backup file : You do not have a backup file.'
	print 'Previous package removal done successfully!\n'
	
# Post installation
def layout_help():
	""" Guiding after installation """
	print '''
	* Go to System > Preferences > Keyboard, click on Keyboard, then
	Keyboard Preferences Window would be appeared.

	* Go to Layout Tab and click on Add button. Choose a Layout Myanmar 
	and press Add button. You will have both US English Layout and 
	Myanmar Layout.
	
	* To get keyboard switching, press Layout Options in the Layout Tab 
	of Keyboard Preferences.
	* Check e.g. Shift+Ctrl Change Layout in Layout Switching.
	
	* To get Keyboard Indicator on your panel, right-click on Panel and 
	click on Add to Panel. Search Keyboard Indicator and click it to add. 
	You will see Keyboard Indicator on your Panel.

'''

if __name__ == '__main__':

	"""	FONTNAME is `mm3` and module name is `mm3-keyboard.py` because
		this package is shipped with mm3 font and xkeyboard.
		If you wish to use this module for another font package, you may need 
		to change FONTNAME and other necessory modifications in name `mm3`
        to your font name or you can make better module.
	"""

	FONTNAME = 'mm3'
	
	# asking what to do ( install or uninstall, something like that)
	print "You are about to press..."
	while 1:
		ans = raw_input('[i] install, [r] remove, [h] layout help, [q] exit : ')
		if ans == 'i':
			print '\nProceeding installation...\n'
			remove()
			install()
			print '''Installation is finished!\n
You may NEED to Log Out or Restart your system to correct your keyboard.\n'''

		elif ans == 'r':
			print '\nProceeding uninstallation...\n'
			remove()
		elif ans ==  'h':
			print '\nProceeding keyboard layout option help...'
			layout_help()
		elif ans == 'q':
			sys.exit('\nHave a nice day, Good bye!\n')
		else:
			print '\nPlease press *small letter* [i] [r] [h] [q] !\n'
