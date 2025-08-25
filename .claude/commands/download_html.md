Think harder to perform following actions:
1. take a HTML web page url $ARGUMENTS as input and read it
2. continue only if this is a valid HTML page and not a PDF or another online file type
3. make a note of metadata like original source url, keywords, title, description
4. create a destination folder html/kebab-case-title/
5. focus on the main article and ignore everything else including navigation, sidebar, footer, ads
6. extract the html representing the main article
7. make a html well formed with minimal doctype, root, head sections 
8. save source metadata in the head section
9. save the html in the destination folder
10. download images within the article, save in images/ folder wihin the destination folder
