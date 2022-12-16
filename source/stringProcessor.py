class PSStringProcessor:
  def transform(textToEdit):
    return textToEdit.split("\\")

  def process(self, userInput):
    a=0
    result = ""

    for actVal in PSStringProcessor.transform(userInput):
      #print("[" + str(a) + "]: " + actVal)
      if " " in actVal:
          result = result + "\\'" + actVal + "'"
          #print("-> must be surrounded")
      else:
        if a != 0:
          result = result + "\\"

        result = result + actVal
      a=a+1

    return result

processor = PSStringProcessor()
#print("Result: " + processor.process())