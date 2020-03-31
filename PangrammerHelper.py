'''
Pangrammer Helper
By Mark Simonson, v. 1.1, March 13, 2012
Thanks to Frederik Berlaen for help with hooking up to Space Center

Simple Python version of a Flash/ActionScript "app" I first did in 2003:
http://www.ms-studio.com/Animation/pangrammerhelper.html

Purpose is to help you write pangrams--sentences that contain all the letters
of the alphabet.

Type in the window. The alphabet will shrink as you use up the letters.
Current pangram length displayed at bottom. If you have a Space Center window
open, its current text will be used and updated as you compose your pangram.

Note: It doesn't do anything with spelled out glyph names (e.g., "/space"
or "/exclam").
      It's only designed to work with literal text you can type directly.
      Non-alphabetic characters are not included in the count for
      pangram length.

Small update by Frank Grießhammer on June 12, 2014:
Add support for mixed-case pangrams
Add support for non-ASCII characters
'''

import vanilla
import string
from mojo.UI import CurrentSpaceCenter

alphabetSetMixed = string.ascii_letters
alphabetSetLower = string.ascii_lowercase


class PangrammerHelper(object):

    def __init__(self):

        self.alphabetSet = alphabetSetMixed

        # set up window
        self.w = vanilla.Window((400, 150), "Pangrammer Helper")
        # set up remaining letters display
        self.w.alphabet = vanilla.TextBox((15, 15, -15, 20), self.alphabetSet)
        # set up text field, inserting Space Center text if available
        if CurrentSpaceCenter() is None:
            pangram = "Type your pangram here"
        else:
            sp = CurrentSpaceCenter()
            pangram = sp.getRaw()
        self.w.pangramEditor = vanilla.TextEditor(
            (15, 40, -15, 70), pangram, callback=self.textEditorCallback)
        self.w.counter = vanilla.TextBox(
            (-250, 110, -15, 20), "Pangram length: 0", alignment='right')
        self.w.checkBox = vanilla.CheckBox(
            (15, 110, -15, 20), "Mixed case",
            callback=self.checkBoxCallback, value=True)
        self.w.open()
        # set remaining letters and counter to reflect contents of text field
        self.textEditorCallback(self)

    def checkBoxCallback(self, sender):
        if sender.get() == 1:
            self.alphabetSet = alphabetSetMixed
        else:
            self.alphabetSet = alphabetSetLower

        self.w.alphabet.set(
            self.getRemainingLetters(self.w.pangramEditor.get()))

    def textEditorCallback(self, sender):
        pangram = self.w.pangramEditor.get()
        self.w.alphabet.set(self.getRemainingLetters(pangram))

        # determine and display pangram length
        self.w.counter.set("Pangram length: %d" % len(pangram))

        # update Space Center text
        if CurrentSpaceCenter() is not None:
            sp = CurrentSpaceCenter()
            sp.setRaw(pangram)

    def getRemainingLetters(self, pangram):

        # determine and update list of unused letters
        remainingLettersList = list(set(self.alphabetSet) - set(pangram))
        remainingLettersList.sort()
        remainingLetters = ''.join(remainingLettersList)
        return remainingLetters


PangrammerHelper()