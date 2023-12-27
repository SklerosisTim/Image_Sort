# Image_sort
An assistant program for ***manually*** sorting images into multiple folders.
It does not sort images automatically, but only helps to save time on this.
Instead of manually moving images in Windows Explorer, taking a long time to select a path and navigate through the file system, you do it with one movement and a mouse click.
### Features:
- The image is transferred by clicking on the corresponding button, in one motion.
- Setting up these buttons is extremely simple, you choose their names and location yourself.
- You can create a huge number of buttons (up to 441 pieces).
- Detailed statistics on the number of images in each folder are displayed.
### To get started, you need:
- Select the `working folder` from which the images will be taken for sorting.
- Select the `save folder` where the subfolders will be created and the images will be placed in them.
- Edit the file `buttons.txt` to create buttons. Each button will place an image in a subfolder, with its own name.
### Example of editing `buttons.txt`:
```
Car Volvo Ford Nissan Porsche
Animal Cat Dog Squirrel Parrot
People Mom Dad Brother Sister
```
The first word in the line is the *parent* button, all following it will be *child* buttons. When you cursor hover the parent button, the child buttons will be shown.
Thanks to this, you can place 21 parent buttons, and 21 child buttons in each of them. Total 441 buttons.
![](https://ibb.co/YjRqcYJ)