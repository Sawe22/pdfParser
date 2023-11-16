# pdfParser


Parses PDF into abstract, intro, methodology, results and colclusion section. Places result into json file. 

To use, run the .py file, and then run "curl -X POST -F "file=@-PathToPDF-" http://localhost:5000/upload".

Replace -PathToPDF- with path to file.

Limited to sections explicitly being mentioned. For instance, with the provided pdf, "concluding remarks" does not go into conclusion, as 
keyword "conclusion" not present.
