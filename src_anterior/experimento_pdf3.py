import fitz

### READ IN PDF
doc = fitz.open("input.pdf")

for page in doc:
    ### SEARCH
    text = "Sample text"
    text_instances = page.search_for(text)

    ### HIGHLIGHT
    for inst in text_instances:
        highlight = page.add_highlight_annot(inst)
        highlight.update()


### OUTPUT
doc.save("output.pdf", garbage=4, deflate=True, clean=True)

pdfIn = fitz.open("page-4.pdf")

for page in pdfIn:
    print(page)
    texts = ["SEPA", "voorstelnummer"]
    text_instances = [page.search_for(text) for text in texts] 
    
    # coordinates of each word found in PDF-page
    print(text_instances)  

    # iterate through each instance for highlighting
    for inst in text_instances:
        annot = page.add_highlight_annot(inst)
        # annot = page.add_rect_annot(inst)
        
        ## Adding comment to the highlighted text
        info = annot.info
        info["title"] = "word_diffs"
        info["content"] = "diffs"
        annot.set_info(info)
        annot.update()


# Saving the PDF Output
pdfIn.save("page-4_output.pdf")