This is for quality checking image scripts. Its setup to be build as a desktop app.   
Currently finding black lines and if any are found it will create a .txt file with the file names.  

Clone the repository.  

Open a terminal window.  

Setup a virtual environment then install the dependencies from the requirement.txt file.  

Navigate to the folder with the main.py file and then run:

```
pyinstaller --windowed --onefile --name "Black Line Finder" main.py
```

This will create a dist folder with the app in it (.exe for windows, .app for MAC).  
