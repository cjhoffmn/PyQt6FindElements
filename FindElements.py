'''Searches PyQt6 ui module for elements and creates a list for connecting elements for a PyQt6 window application.'''
from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
import sys, os

class MnWin(QMainWindow):
    def __init__(self):
        super(MnWin, self).__init__()

    def file_select(self) -> Path:
        '''Allows user to select folder where the [PyQt6_ui].py converted by uic from the QtDesigner.ui file is stored'''
        fname = QFileDialog.getOpenFileName(self ,"Find a File to read", ".py")
        if fname:
            path_to_module = Path(fname[0])
            return path_to_module

def main():
    ''' main() will create a list of element names fom the PyQt6_ui.py ('uifile') file chosen by the user.  It will
        1.) Search the uifile for element names by finding the occurences of the "setObjectName()" method.  Thes are
            the object names created either Qt Designer or by the coder of the uifile.  
        2.) Create a list of the names of of those elments.
        3.) Uses that list crete a second list by searching the uifile for rerences to where those elements were set to objects by finding 
            the use of " = " in lines with the elements' names.
        4.) Creates a new list of lists combining the two items above and then removing any items where there was no object set for
            an element name
        5.) It then reduces the element type text down to object reference and recombines the names and the element types.
        6.) It then uses that list to create code for injection into a new QWidget and prints it to the console for easy copying.'''
    #using PyQt6 to instantiate a folder picker
    app = QApplication(sys.argv)
    mw = MnWin() #object needs to be created, but window does not need to be created.

    '''list of user defined terms that are included in the underlying PyQt6_ui.py ('uifile') file that are tags by the 
    developer to identify various element types.  If set all the way from QT Designer then included here the 
    list to copy will be filtered to the highly relevant.'''

    srch_term_list = ["btn","lbl","text_edit","cmbbox", "action"]

    #get user PyQt6_ui.py file
    path_to_module = mw.file_select()
    with open(path_to_module) as uifile:
        alltext = uifile.readlines()

    #list of names of elements in the uifile that are set by the setObjectName method
    elem_nms_setObj = [ln.strip('"').strip() for ln in 
                        [ln.split('")',1)[0] for ln in 
                            [ln.split('e(',1)[1] for ln in 
                                [ln for ln in alltext if ln.find("setObjectName") != -1]
                            ]
                        ]
                    ]
    #filtered to the list of the search terms list
    filteredlist = [nms for nms in elem_nms_setObj if any(x in nms for x in srch_term_list)]

    #Find the lines that are setting the element names to classes/objects in the uifile
    elmnt_typ_lines =   [str(etln).split("= ",1) for etln in 
                            [[ln for ln in alltext if ln.find(en + ' = ') !=-1] for en in filteredlist]
                        ]
    et_en_setObj = list(zip(filteredlist, elmnt_typ_lines))
    
    #Filter the list for any lines that were included that had a set operator but are not elements
    et_en_objs = [en_et for en_et in et_en_setObj if en_et[1][0] != '[]']

    #split the list back apart into names and lines to so the lines can be reduced to the object name only
    obj_et = [en_et[1] for en_et in et_en_objs] #list of the element types
    obj_en = [en_et[0] for en_et in et_en_objs] #list of the element names
    obj_et2 = [str(et[1]).split("(",1)[0] for et in obj_et]
    
    #recombined list after type was cleaned
    en_et_list = list(zip(obj_en, obj_et2))

    #create text for code to be copied and printing them to console
    assigned = [f'self.{en_et[0]} = self.findChild({en_et[1]},"{en_et[0]}")' for en_et in en_et_list]
    connected = [f'self.{en_et[0]}.[ACTION].connect(self.[MTHD for {en_et[0]}])' for en_et in en_et_list]
    print_lists_to_copy(assigned, connected)
    #print(et_en_objs)

def print_lists_to_copy(assigned: list, connected: list):
    '''Prints the lists created above to the console to be copied easily to the PyQt6 window where the elements 
        are to be assigned and connected'''
    os.system('cls')
    print(f'Assign:')
    for ln in assigned:
        print(f'{ln}')
    print(f'Connect:')
    for ln in connected:
        print(f'{ln}')

if __name__ == "__main__":
    main()


