# coding=utf-8

import os, zipfile, fnmatch

import datetime
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileMerger
import shutil
import time


source_location = "/home/ibrahim/Desktop/vasanth"
target_location = "/home/ibrahim/Desktop/vasanth_output"
intermediate_pdf = "ibrahim.pdf"


class PDFGenerator(object):

    def extract_child_dir(self, temp_dir, rootPath):
        for i in temp_dir:
            temp_root_path = os.path.join(rootPath, i)
            print ("Child Extraction services started - {0}".format(temp_root_path))
            self.extract_dirs(temp_root_path, "*.ZIP")
            print ("Child Extraction services completed - {0}".format(temp_root_path))

    def extract_dirs(self, root_path, pattern):
        temp_dir = []
        for root, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                print(os.path.join(root, filename))
                zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
                # zip_ref.close()
                temp_dir.append(os.path.splitext(filename)[0])
        return self.extract_child_dir(temp_dir, root_path)

    def create_pdf(self, root_path, pattern):
        for root, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                print(os.path.join(root, filename))
                try:
                    out_file = os.path.join(root, filename)
                    im = Image.open(out_file)
                    im = im.convert('RGB')
                    save_img_path = os.path.join(root, os.path.splitext(filename)[0] + ".pdf")
                    im.save(save_img_path, "PDF", resolution=100.0)
                except Exception, e:
                    print e
        return 1

    def PDFmerge(self, pdfs, output, root):

        # creating pdf file merger object
        pdfMerger = PdfFileMerger()
        # appending pdfs one by one
        for pdf in pdfs:
            # with open(os.path.join(root, pdf), 'rb') as f:
            # with open(PdfFileReader(os.path.join(root, pdf)), 'rb') as f:
            try:
                pdfMerger.append(PdfFileReader(os.path.join(root, pdf)), 'rb')
            except Exception as e:
                print (e)
        # writing combined pdf to output pdf file

        with open(os.path.join(root, "ibrahim.pdf"), 'wb') as f:
            # import ipdb;
            # ipdb.set_trace();
            pdfMerger.write(f)

    def merge_pdf(self, root_path, pattern):
        for root, dirs, files in os.walk(root_path):
            # for filename in fnmatch.filter(files, pattern):
            temp_files = fnmatch.filter(files, pattern)
            if len(temp_files) > 0:
                self.PDFmerge(temp_files, root.split('/')[-1], root)
            # print(os.path.join(root, filename))
        return 1

    def generate_output(self, root_path, pattern, target_location):
        # import ipdb;ipdb.set_trace();
        today = datetime.datetime.now()
        parent_folder_name = today.strftime('%m-%Y')
        child_folder_name = today.strftime('%d-%m-%Y')
        output_location = os.path.join(target_location, parent_folder_name, child_folder_name)
        if not os.path.exists(output_location):
            os.makedirs(output_location)
        for root, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                output_location_temp = os.path.join(output_location, root.split('/')[-1])
                if not os.path.exists(output_location_temp):
                    os.makedirs(output_location_temp)
                shutil.copy2(
                    os.path.join(root, filename),
                    os.path.join(
                        output_location_temp,
                        os.path.join(output_location_temp, output_location_temp.split('/')[-1] + ".pdf")
                    )
                )
        return 1

    def generate_output_xml(self, root_path, pattern, target_location):
        # import ipdb;ipdb.set_trace();
        today = datetime.datetime.now()
        parent_folder_name = today.strftime('%m-%Y')
        child_folder_name = today.strftime('%d-%m-%Y')
        output_location = os.path.join(target_location, parent_folder_name, child_folder_name)
        # if not os.path.exists(output_location):
        #     os.makedirs(output_location)
        for root, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                output_location_temp = os.path.join(output_location, root.split('/')[-1])
                if not os.path.exists(output_location_temp):
                    os.makedirs(output_location_temp)
                shutil.copy2(os.path.join(root, filename), output_location_temp)
        return 1


pdf_generator = PDFGenerator()

if __name__ == "__main__":
    start_time = time.time()
    print ("************************************************")
    print ("Extraction services started")
    pdf_generator.extract_dirs(source_location, "*.ZIP")
    print ("Extraction services completed")
    print ("************************************************")
    print ("Extraction pdf services started")
    pdf_generator.create_pdf(source_location, "*.TIF")
    print ("************************************************")
    print ("Extraction pdf services completed")
    print ("************************************************")
    print ("Extraction pdf merge services started")
    pdf_generator.merge_pdf(source_location, "*.pdf")
    print ("Extraction pdf merge services completed")
    print ("************************************************")
    print ("Generate Output services started")
    pdf_generator.generate_output(source_location, intermediate_pdf, target_location)
    print ("Generate Output services completed")
    print ("************************************************")
    print ("************************************************")
    print ("Generate Output services XML started")
    pdf_generator.generate_output_xml(source_location, "*.XML", target_location)
    print ("Generate Output services XML completed")
    print ("************************************************")
    end = time.time()
    elapsed_seconds = float("%.2f" % (end - start_time))
    print('elapsed seconds: {0}'.format(elapsed_seconds))