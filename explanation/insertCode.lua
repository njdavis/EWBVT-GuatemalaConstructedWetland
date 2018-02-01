-- Pandoc filter to add the contents of external text files Useful for charts and tables. call by making a codeBlock with the class titled "insertExtFile" and the contents equal to the location  of the file you wish to add
-- ~~~~~~~ {#this .insertExtFile .read}
-- ../Graphs and Charts/charts/Kadlec 21-1 Table.txt
-- ~~~~~~~


function CodeBlock(block)

	if block.classes[1] == "insertExtFile" then
			
		local f = assert(io.open(block.text, "r"))
		local content = f:read("*all")
		f:close()

		local document = pandoc.read(content, "markdown")
	
		return document.blocks
	end
end


