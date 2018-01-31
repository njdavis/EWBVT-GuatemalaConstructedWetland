import pdb
import pypandoc, os


#compiling 
print("Compiling and running main.py")
#python3 ../code/main.py

print("Assembling markdown file")
#pip3 install filter_pandoc_run_py

#os.system("pandoc markdownWetlandNotes.txt --filter pandoc-fignos --filter pandoc-tablenos --filter pandocFilter.py -o wetlandNotes.pdf")


filters = ['pandoc-fignos', 'pandoc-tablenos', 'pandocFilter.py']
pdoc_args = []
output = pypandoc.convert_file('markdownWetlandNotes.txt',
                         to='pdf', format='md',
                         outputfile='wetlandNotes.pdf',
                         extra_args=pdoc_args,
						 filters=filters)

