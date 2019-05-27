# coding: UTF-8
import urllib.request, urllib.error
import io,sys,os
import datetime
import zipfile
#import mysql.connector
import csv
import configparser



def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    try:
        # sys.argv[1] is output csv path
        sp = StockPrice(sys.argv[1])
        sp.downloadFile()
        sp.extractFile()
        sp.combartFile()
        #sp.importDB()
        print("Success!")
    except Exception as e:
        print("Error!")
        print(e.args)



class StockPrice():
    title = ""
    url = ""
    output_file_name = ""
    output_dir_path = ""
    dbcon = object

    def __init__(self, path):
        today = datetime.date.today()
        yyyy = today.strftime("%Y")
        yy = yyyy[2:]
        mm = today.strftime("%m")
        dd = today.strftime("%d")
        self.title = "T" + yy+mm+dd
        self.url = "http://souba-data.com/d_data/" + yyyy + "d/" + yy + "_" + mm + "d/" + self.title + ".zip"
        self.output_file_name = yyyy + "-" + mm + "-" + dd + "_kabuka_output.csv"
        self.output_dir_path = path
        print("Current Directory :" + os.getcwd() )
        os.chdir(path)
        print("Current Directory:" + os.getcwd())

    def downloadFile(self):
        print("Download Start...")
        print("URL:" + self.url)
        urllib.request.urlretrieve(self.url, "{0}".format(self.title))

    def extractFile(self):
        print("Extractall ..." + self.title)
        with zipfile.ZipFile(self.title) as existing_zip:
            existing_zip.extractall()

    def combartFile(self):
        print("Modify ...")
        output = ["code,market,name,business,opening,high,low,ending,volume,trading_value"]
        with open(self.title + ".csv", encoding="shift_jis") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            line = ""
            for row in reader:
                line = row[1] + ","    # code
                line += row[9] + ","   # market
                line += row[3] + ","   # name
                line += ""     + ","   # business
                line += row[4] + ","   # opening
                line += row[5] + ","   # high
                line += row[6] + ","   # low
                line += row[7] + ","   # ending
                line += row[8] + ","   # valume
                line += ""             # trading_value
                output.append(line)
        with open(self.output_file_name, mode='w', encoding='utf8') as f:
            f.write('\n'.join(output))




if __name__ == '__main__':
    main()