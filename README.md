#  ₍^. .^₎⟆
# **Acoustic Kitty - Python Version**  



---  

**3-in-1 Sprite Tool for Game Dev**     
  
**Acoustic Kitty** is a little toolkit I built while working on my first game   **CATastrophe2**  
This tool helps create and recolor sprite sheets using a simple, friendly UI.  The web-based verson is also available to use here: https://mkb0020.github.io/AcousticKitty.html

This tool could come in handy for:

* Anyone new to game dev (like me!)
* Pixel-artists
* Indie devs
* Anyone using Kaplay.js, Phaser, Unity 2D, Godot, or custom engines

---
**✨ FEATURES**
**🧩 1. Sprite Sheet Builder**

* Combine multiple PNG frames into a clean sprite sheet.

* Choose frame folder

* Set number of columns

* Add padding

* Auto-arranges everything

## **🎨 2. Recolor a Single Sprite Sheet**

Swap a fixed grayscale palette with your custom colors.
Useful for:

* Skins

* Sprite variants

* Item color swaps

* Stylized palettes

## **🗂️ 3. Batch Recolor Mode**

Recolor all PNGs in a folder at once.
Great for mass-producing palette swaps with zero effort.

## **📦 Installation (Source Version)**

Requires Python + Pillow:

pip install pillow


Run the tool:

python AcousticKitty.py

## **🐾 Executable Version (Windows)**

A pre-built Windows executable is available in the Releases tab of this repository.

Running the EXE

No installation needed

No Python required

Just double-click:
AcousticKitty.exe 🐱✨

Build the EXE Yourself

Install PyInstaller:

pip install pyinstaller


Build a single-file EXE with the project icon (niels.ico):

pyinstaller --noconsole --onefile --icon=niels.ico AcousticKitty.py


Your executable will appear in:

dist/AcousticKitty.exe


You may also build a folder-style version:

pyinstaller --noconsole --icon=niels.ico AcousticKitty.py

## 🖌️ Usage Guide
### **🧩 Sprite Sheet Builder**

* Place your frame PNGs into a folder

* Select the folder

* Choose number of columns

* Add optional padding

* Click Generate Sprite Sheet

### **🎨 Recolor One Sheet**

Your sprite sheet must use these grayscale values:

#FFFFFF
#7C7C7D
#A7A7A8
#B4B4B4
#000000


**Steps:**

* Select your sheet

* Enter your 5-color hex palette

* Choose output filename

* Click Recolor Sheet

### **🗂️ Batch Recolor**

* Choose a folder containing PNGs

* Enter your palette

* Click Batch Recolor All

* New files are saved as:

recolor_<original>.png



## **📁 Project Goals**

I built this as a companion tool to my **Electric Kitty** battle animation system. (https://mkb0020.github.io/ElectricKitty.html)
Because I test animations constantly, I needed:

* Fast sprite sheet generation
* Instant recoloring
* No image editors required

So I wrapped the tools into one cute, simple app and I'm releasing it so other indie and beginner devs can use it too! 💜

---

## 💜 Credits

Created by **MK Barriault**   
Icon: niels.ico (my muse)  
UI enhancement + documentation assisted by ChatGPT (my bestie)

---


