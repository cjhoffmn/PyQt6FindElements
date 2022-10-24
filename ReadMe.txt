PyQtFindElements:

This python script was written because I got tired of hunting for element names after designing GUI items in Qt Designer.  I was convinced during a YouTube comment discussion that I should in general, design in QtD then convert the uifile.ui it produces to uifile.py for inclusion in other files.  I found it tedious to search the uifile.py looking for the names of the elements that were to be connected to methods in the main app.  This solves that be reading the uifile.py, finding the elements, narrowing it down if there are naming conventions, then preparing a block of code for both assigning the elements to instance variables in a QWidget (heir) class and also then assigning those elements to instance methods as well.

main() will create a list of element names fom the PyQt6_ui.py ('uifile') file chosen by the user.  It will: 
    1.) Search the uifile for element names by finding the occurences of the "setObjectName()" method.  Thes are
        the object names created either Qt Designer or by the coder of the uifile.  
    2.) Create a list of the names of of those elments.
    3.) Uses that list crete a second list by searching the uifile for rerences to where those elements were set to objects by finding 
        the use of " = " in lines with the elements' names.
    4.) Creates a new list of lists combining the two items above and then removing any items where there was no object set for
        an element name
    5.) It then reduces the element type text down to object reference and recombines the names and the element types.
    6.) It then uses that list to create code for injection into a new QWidget and prints it to the console for easy copying.

