from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil
import logging
import time
logging.basicConfig(level=logging.DEBUG)

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
file_path = os.path.join(path,"xmlassignemnt","app","files")
move_path = os.path.join(path,"xmlassignemnt","app","move")

def get_file(file_name):
    try:
        xmlfile =   os.path.join(file_path,file_name)
        DOMTree = xml.dom.minidom.parse(xmlfile) 
        return xmlfile
    except Exception as err:
        print(err)
        return None

def move_file(file_name):
    try:
        src_path = os.path.join(file_path,file_name)
        dst_path = os.path.join(move_path,file_name)
        shutil.move(src_path, dst_path)
    except Exception as err:
        print(err)
        return False

def parseXML(xmlfile):
    DOMTree = xml.dom.minidom.parse(xmlfile) 
    collection = DOMTree.documentElement
    Metadata = collection.getElementsByTagName("Metadata")
    for Metadat in Metadata:
        if Metadat.getElementsByTagName('AMS')[0].getAttribute("Provider_ID") == "0007":
            App_Data = Metadat.getElementsByTagName("App_Data")
            price = None
            length = None
            for app in App_Data:
                if app.getAttribute("Name") == "Maximum_Viewing_Length": 
                    length = app.getAttribute("Value")
                if app.getAttribute("Name") == "Suggested_Price":
                    price = app.getAttribute("Value") 
            if length == "02:00:00" and price == "5.98":
                logging.info('the xml is correct')
            elif price is not None or length is not None:
                logging.warning('the xml is incorrect')
                for app in App_Data:
                    if app.getAttribute("Name") == "Suggested_Price":
                        app.setAttribute("Value","5.98")  
                        with open( xmlfile, "w" ) as fs: 
                            fs.write( DOMTree.toxml() )
                            fs.close() 
    
    

def main():
    file_list = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f)) and f.endswith('.xml')]
    if len(file_list) == 0:
        logging.info("No File is Persent")
        return True
    
    for file in file_list:
        status = get_file(file)
        if status:
            parseXML(get_file(file))
            move_file(file)
            return True
    
    main()
    
def func_main():
    main()
    time.sleep(60) #Call Function again 1 Min
    func_main()

if __name__ == '__main__':
    func_main()