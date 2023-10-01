import os

def transform(textToEdit):
    return textToEdit.split("\\")

def process(userInput):
  a=0
  result = ""

  userInputSplit = transform(userInput)
  
  for actVal in userInputSplit:
    # print("[" + str(a) + "]: " + actVal)
    if " " in actVal:
        
      if a != userInputSplit.__len__()-1:
        result = result + "\\'" + actVal + "'"
        # print("-> must be surrounded")
      else:
        # split actval into filename and extension
        # print("-> filename -> only the filename must be surrounded")
        
        filename, file_extension = os.path.splitext(actVal)
        #filename, file_extension = actVal.split(".")
        result = result + "\\'" + filename + "'" + file_extension + ""
    else:
      if a != 0:
        result = result + "\\"

      result = result + actVal
    a=a+1

  return result