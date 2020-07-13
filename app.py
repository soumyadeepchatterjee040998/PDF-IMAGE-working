import streamlit as st
import zlib,base64
import os
import PyPDF2
import io
import numpy as np
import fitz
from PIL import Image
from typing import Dict,List
from fpdf import FPDF


def none():
    st.title("DO NOT SHARE ANY SENSITIVE INFORMATION")
    st.title(".....This is made only for EDUCATIONAL POURPOSE ONLY....")
    st.subheader(">>>We TRY to FIX THE POSSIBLE AVAILABLE BUGS<<<<<<")
    
    st.header("1. COMPRESS")
    st.image("images1.jpg",caption="WE can compress your PDF with encoding ")
    st.header("2. DECOMPRESS")
    st.image("images2.jpg",caption="WE can decompress your PDF with decoding ")
    st.header("3. SPLIT")
    st.image("images3.jpg",caption="WE can split your PDF into samll PDFs ")
    st.header("4. MERGE")
    st.image("images4.jpg",caption="WE can MERGE small PDFs to a LARGER ONE ")
    st.header("5. PDF READER")
    st.image("images5.jpg",caption="WE can read your PDF")
    st.header("6. DELETE A PAGE FROM PDF")
    st.image("images6.jpg",caption="WE can delete a page(or pages) your PDF ")
    st.header("7. CONVERT IMAGE(S) TO PDF")
    st.image("images7.jpg",caption="WE can convert image(s) to pdf  ")
    st.header("8. CONVERT PDF TO IMAGES(s)")
    st.image("images8.jpg",caption="WE can convert a PDF into IMAGES ")
    


def compress(level):#compression and ecryption    pdf->txt
    file = st.file_uploader("Upload your pdf file",type=("pdf"))
    submit = st.button("upload")
    dwnld = st.button("Download")
    flag = False
    if submit | dwnld:
        if file:
            
            pdf = PyPDF2.PdfFileReader(file)
            output = open("intermediate.pdf","wb")
            out = PyPDF2.PdfFileWriter()
            for i in range(pdf.numPages):
                out.addPage(pdf.getPage(i))
            out.write(output)
            
            file = open('intermediate.pdf','rb').read()
            text = base64.b64encode(zlib.compress(file,level=level))
            out = open('Compressed.txt','wb')
            out.write(file)
            out.close()
            st.success("Now you can download")
            if dwnld:
                txt = open('Compressed.txt','rb').read()
                b64 = base64.b64encode(txt).decode()
                href = f'<a href="data:txt;base64,{b64}" download>Download</a>'
                st.markdown(href,unsafe_allow_html=True)
                flag = True
        else:
            st.error("Please upload your pdf file first")
    return flag
    
def decompress():#decryption and decompression  txt->pdf
    file = st.file_uploader("Upload a text file",type=("txt"))
    submit = st.button("Submit")
    dwnld = st.button("Download")
    flag = False
    if submit|dwnld:
        if file:
            file = file.read()
            intr = open('intr.txt','wb')
            intr.write(file)
            intr.close()
            
            text = open('intr.txt','rb').read()
            file = zlib.decompress(base64.b64decode(text))
            output = open("Decompressed.pdf","wb")
            output.write(file)
            output.close()
            
            st.info("Please ADD \".pdf\" extension to download this file")
            if dwnld:
                pdf = open('Decompressed.pdf','rb').read()
                b64 = base64.b64encode(pdf).decode('utf-8')
                href = f'<a href="data:pdf;base64,{b64}" download>Download</a>'
                st.markdown(href,unsafe_allow_html=True)
                flag = True
        else:
            st.error("Please upload your pdf file first")

    return flag

def split():# 1 PDF --->> Many PDFs   
    file = st.file_uploader("Upload your pdf file",type=("pdf"))
    submit = st.button("SPLIT")
    view = st.button("VIEW")
    flag = False
    total = 0
    if submit|view:
        if file:
            pdf = PyPDF2.PdfFileReader(file)
            output = open("intermediate.pdf","wb")
            out = PyPDF2.PdfFileWriter()
            total = pdf.numPages
            for i in range(total):
                out.addPage(pdf.getPage(i))
            out.write(output)
            output.close()
            
            file = open('intermediate.pdf','rb')
            pdf = PyPDF2.PdfFileReader(file)
            for i in range(pdf.numPages):
                name = "split_pdf_page_{}.pdf".format(i)
                output = open(name,'wb')
                out = PyPDF2.PdfFileWriter()
                out.addPage(pdf.getPage(i))
                out.write(output)
                output.close()
                
            st.success("Compleated")
            if view:
                for i in range(total):
                    name = "split_pdf_page_{}.pdf".format(i)
                    file = open(name,"rb")
                    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
                    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
                    st.markdown(pdf_display, unsafe_allow_html=True)
                    flag = True
        else:
            st.error("Please upload your pdf file first")
    return (flag,total)


@st.cache(allow_output_mutation=True)
def get_static_store_() -> List:
    return []

def merge():#Many PDF --->> One PDF
    static_list = get_static_store_()
    file = st.file_uploader("Upload a PDF file",type=("pdf"))
    st.info("Please browse more images if required. Note:-->>The images store internally.No need to worry")
    st.info("MAKE SURE CLEAR THE LIST FROM CACHE TO START A FRESH")
    submit = st.button("submit")
    clear = st.button("clear LIST")
    view = st.button("Show PDF")
    flag = False
    if submit:
        if file:
                static_list.append(PyPDF2.PdfFileReader(file,strict=False))
        else:
            st.warning("Please upload a PDF File")
    if clear:
        static_list.clear()
    if view:
        if len(static_list)!=0:
            output = open("Merge.pdf","wb")
            out = PyPDF2.PdfFileMerger()
            for i in range(len(static_list)):
                out.append(static_list[i])
            out.write(output)
            output.close()
        
            flag = True
            file = open("Merge.pdf","rb")
            base64_pdf = base64.b64encode(file.read()).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
            st.markdown(pdf_display, unsafe_allow_html=True)
            pdf = open('Merge.pdf','rb').read()
            b64 = base64.b64encode(pdf).decode('utf-8')
            href = f'<a href="data:pdf;base64,{b64}" download>Download This PDF</a>'
            st.markdown(href,unsafe_allow_html=True)
        else:
            st.warning("Make sure you UPLOAD atleast 1 PDF")

    return flag    
    
def pdf_reader():
    file = st.file_uploader("upload a pdf file",type=("pdf"))
    submit = st.button("SUBMIT")
    view = st.button("VIEW PDF")
    flag = False
    if submit | view :
        if file:
            pdf = PyPDF2.PdfFileReader(file)
            output = open("intermediate.pdf","wb")
            out = PyPDF2.PdfFileWriter()
            for i in range(pdf.numPages):
                out.addPage(pdf.getPage(i))
            out.write(output)
            output.close()
            st.success("Now you can view")
            if view:
                file = open("intermediate.pdf","rb")
                base64_pdf = base64.b64encode(file.read()).decode('utf-8')
                pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
                st.markdown(pdf_display, unsafe_allow_html=True)
                flag = True
        else:
            st.error("Please upload your pdf file first")
    return flag

def delete_page(list_):
    file = st.file_uploader("Upload your pdf file",type=("pdf"))
    submit = st.button("SUBMIT")
    delpage = st.button("DELETE PAGE(s)")
    view = st.button("View")
    flag = False
    total = 0
    if submit|delpage|view:
        if file:
            try:
                if len(list_)!=0:
                    pdf = PyPDF2.PdfFileReader(file)
                    output = open("intermediate.pdf","wb")
                    out = PyPDF2.PdfFileWriter()
                    total = pdf.numPages
                    for i in range(total):
                        out.addPage(pdf.getPage(i))
                    out.write(output)
                    output.close()
                    st.success("Now you can DELETE Page(s)")
                    list_ = list(np.unique(np.int32(list_)))
                    st.success("these are the pages that will be deleted"+str(list_))
                    if delpage:
                        output = open("PDF_after_DELETE.pdf",'wb')
                        input_ = open("intermediate.pdf",'rb')
                        pdf = PyPDF2.PdfFileReader(input_)
                        out = PyPDF2.PdfFileWriter()
                        i = 0
                        if len(list_)<=total:
                            while i<total:
                                try:
                                    if list_[0]<=total and i!=list_[0]-1:
                                            out.addPage(pdf.getPage(i))
                                    else:
                                        list_.pop(0)
                                    i += 1
                                except:
                                    for k in range(i,total):
                                        out.addPage(pdf.getPage(k))
                                    break
                            st.success("Delete compleate")
                        else:
                            st.error("The length of the list must be less than or euqual to the total page present inside the pdf")
                        out.write(output)
                        output.close()
            except:
                st.warning("No page is selected to delete")
            if view:
                try:
                    file = open("PDF_after_DELETE.pdf","rb")
                except:
                    file = open("intermediate.pdf","rb")
                base64_pdf = base64.b64encode(file.read()).decode('utf-8')
                pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
                st.markdown(pdf_display, unsafe_allow_html=True)
                flag = True
        else:
            st.error("Please upload your pdf file first")
    return flag


@st.cache(allow_output_mutation=True)
def get_static_store() -> Dict:
    return {}

def image2pdf():
    flag = False
    static_store = get_static_store()
    result = st.file_uploader("Upload jpg/jpeg/png Images", type=("jpg","jpeg","png"))
    st.info("Please browse more images if required. Note:-->>The images store internally.No need to worry")
    if result:
        value = result.getvalue()
        if not value in static_store.values():
            static_store[result] = value
        if st.button("Clear file list"):
            static_store.clear()
        if st.button("make PDF"):
            img = []
            i = 0
            for value in static_store.values():
                Image.open(io.BytesIO(value)).save("sub_pdf_{}.png".format(i))
                _ = Image.open("sub_pdf_{}.png".format(i))
                if _.mode == "RGBA":
                    _ = _.convert("RGB")
                img.append(_)
                i += 1
                
            img[0].save("image2pdf.pdf",save_all = True, quality=100, append_images = img[1:])
            st.success("PDF created")
        try:    
            if st.button("View PDF and Download"):
                file = open("image2pdf.pdf","rb")
                base64_pdf = base64.b64encode(file.read()).decode('utf-8')
                pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
                st.markdown(pdf_display, unsafe_allow_html=True)
                flag = True
        except:
            st.warning("First slect some Image to make a PDF")
            
    return (len(static_store),flag)

def pdf2image():
    file = st.file_uploader("Upload your pdf file",type=("pdf"))
    submit = st.button("SUBMIT")
    view = st.button("View")
    flag = False
    total = 0
    if submit|view:
        if file:
            pdf = PyPDF2.PdfFileReader(file)
            output = open("intermediate.pdf","wb")
            out = PyPDF2.PdfFileWriter()
            total = pdf.numPages
            for i in range(total):
                out.addPage(pdf.getPage(i))
            out.write(output)
            output.close()
            st.success("Now You can view every PAGES as SEPARATE Image")
            st.info("To DOWNLOAD These IMAGES Right-CLICK on the IMAGE itself")
            if view:
                file = fitz.open("intermediate.pdf")
                for i in range(total):
                    page = file.loadPage(i)
                    pix = page.getPixmap()
                    pix.writePNG("pdf2image_{}.png".format(i))
                for i in range(total):
                    img = Image.open("pdf2image_{}.png".format(i))
                    st.image(img,caption="PAGE NO : {}".format(i))
                flag = True
        else:
            st.error("Please upload your pdf file first")
    return (flag,total)
            
def main():
    st.header("PDF-IMAGE Working")
    st.subheader("Thanks For Using")
    opt = st.sidebar.radio("SELECT ONE",["NONE","compress","decompress","split","merge","pdf reader","delete a page from pdf","convert image to pdf","convert pdf to image"])
    if opt=="NONE":
        none()
    if opt=="compress":##compleate
        level = st.slider("level of compression",0,9,0)
        if compress(level)==True:
            os.remove("intermediate.pdf")
            os.remove("Compressed.txt")
            
    if opt=="decompress":
        if decompress()==True:
            os.remove("Decompressed.pdf")
            os.remove("intr.txt")
    
    if opt=="split":
        (flag_,total_) = split()
        if flag_==True:
            os.remove("intermediate.pdf")
            for i in range(total_):
                name = "split_pdf_page_{}.pdf".format(i)
                os.remove(name)

    if opt=="merge":
        if merge() == True:
            os.remove("Merge.pdf")
        
    if opt=="pdf reader":##compleate
        if pdf_reader()==True:
            os.remove('intermediate.pdf')
            
    if opt=="delete a page from pdf":
        st.write("Please mention the PAGE NUMBER of the GIVEN PDF to DELETE ")
        html = f'<div>Note that:<p>1. page number should start from 1</p><p>2. page number should be less or eual to the total pages present</p></div>'
        st.markdown(html,unsafe_allow_html=True)
        list_ = st.text_input("Provide the page number to delete(EX: 5,8,10,1)").split(',')
        if delete_page(list_) ==True:
            os.remove("intermediate.pdf")
            os.remove("PDF_after_DELETE.pdf")   
            
    if opt=="convert image to pdf":
        (count,flag) = image2pdf()
        if flag==True:
            for i in range(count):
                os.remove("sub_pdf_{}.png".format(i))
            os.remove("image2pdf.pdf")
            
    if opt=="convert pdf to image":
        (flag,total) = pdf2image()
        if flag==True:
            os.remove("intermediate.pdf")
            for i in range(total):
                os.remove("pdf2image_{}.png".format(i))
    
if __name__ == '__main__':
    main()
    
    

