import os
import win32com.client as win32
import glob

for path, dirs, files in os.walk('E:\\통상산업조사실(2015.5.1-)\\통상산업조사실(16.02.29~)\\오토데일리 활용방안 연구\\2019년 오토데일리 원본'):
    files = glob.glob('E:\\통상산업조사실(2015.5.1-)\\통상산업조사실(16.02.29~)\\오토데일리 활용방안 연구\\2019년 오토데일리 원본\\*.doc')

    for fname in files:
        word = win32.Dispatch("Word.Application")
       # word.Visible = 0
        filename = fname[-22:-8]

        doc1 = word.Documents.Open(fname)

        DocContents = str(doc1.Content.Text)
        DocContents = DocContents.replace('\r', '\n')
        DocContents = DocContents.strip()

        for line in DocContents.split('\n'):
            if line == '':
                continue
            elif line.startswith('□') or line.startswith('['):
                print(filename + '@' + line)
            else: print(filename + '@@' + line)

           # if line.startswith('□'):
           #     print("\n" + filename + '@' + line, end=" ")
           # else: print(line, end=" ")

        print(' ')

        word.ActiveDocument.Close()
        word.Quit()
        doc1 = ''
        DocContents = ''

