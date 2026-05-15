



# Files
  
Manage your files and folders, open and read files, control their existence and get their meta data.  

*Read this in other languages: [English](Manual_Files.md), [Português](Manual_Files.pr.md), [Español](Manual_Files.es.md)*
  
![banner](imgs/Banner_Files.png)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  

# How to use this module




## Description of the commands

### Open Folder
  
Open folder from a file path
|Parameters|Description|example|
| --- | --- | --- |
|File path  |Open the folder from the specified path|C:/User/Usuario/Folder/|
|Assign result to variable|Variable where the result will be stored|Variable|

### Open File
  
Open file
|Parameters|Description|example|
| --- | --- | --- |
|File path  |Open the file from the specified path|C:/User/Usuario/Folder/File.extension|
|Assign result to variable|Variable where the result will be stored|Variable|

### Get file
  
Ask the user to select a file and get the path
|Parameters|Description|example|
| --- | --- | --- |
|Variable where save path  |When you execute it, or the file explorer opens so that we can select the file, once selected, it provides us with or direct where it is located.|Result|

### Get folder
  
Ask the user to select a folder
|Parameters|Description|example|
| --- | --- | --- |
|Variable where save path  |When executed, the file explorer opens so that we can select the folder we want, once selected, it returns the path where it is located|Result|

### Rename folder
  
Ask the user to select a folder to rename it
|Parameters|Description|example|
| --- | --- | --- |
|Path of the folder to rename |When executing, the folder that we have specified is renamed|C:/User/Folder/|
|New name of the folder|Name of the folder without the path|New name|
|Assign result to variable|Variable where the result will be stored|Variable|

### Read file
  
Reads a plain text file and saves its contents in a variable
|Parameters|Description|example|
| --- | --- | --- |
|File path|Path of the file to read|C:/Users/User/Desktop/file.txt|
|Encoding|Encoding of the file to read. Ex latin-1, utf-8, etc|latin-1|
|Separate lines|Returns the content of a file and stores it in a variable, if the separate lines option is checked, it returns the content of the file within a list and each line is an element within the list|True|
|Assign result to variable|Variable where the obtained value will be stored|Variable|

### Delete folder
  
Delete a folder with all files
|Parameters|Description|example|
| --- | --- | --- |
|File path  |Slect path of the folder to delete|C:/User/Usuario/Folder/|
|Assign result to variable|Variable where the result will be stored|Variable|

### Delete file
  
Delete a file indicating its extension and its name or part of the name
|Parameters|Description|example|
| --- | --- | --- |
|File path  |Path of the file to delete|C:/User/Usuario/Folder/|
|Type of file to delete|Name and extension of the file to delete|name*.pdf|
|Assign result to variable|Variable where the result will be stored|Variable|

### Create Folder
  
Enter the path with name where you want to create the folder
|Parameters|Description|example|
| --- | --- | --- |
|File path|Path where folder are be created|C:/Users/User/Desktop/folder_test|
|Assign result to variable|Variable where the result will be stored|Variable|

### Check existence
  
Check if a file o folder exists
|Parameters|Description|example|
| --- | --- | --- |
|File path  |Address of the folder you want to check for existence|C:/User/Usuario/Folder/|
|Assign result to variable|Variable where the result will be stored|Variable|

### List sorted files
  
CList files and select sort
|Parameters|Description|example|
| --- | --- | --- |
|File path  |Path of the folder from which you want to list the files|C:/User/Usuario/Folder/|
|Sort by|Options to order, Name, Date and Type|Name|
|Assign result to variable|Variable where the list of items in the folder is stored|Variable|

### Search File
  
Returns a list with matches
|Parameters|Description|example|
| --- | --- | --- |
|File path  |Address where the file will be searched|C:/User/Usuario/Folder/|
|Filter by extension|Filter by extension looking for all files with the specified extension|.pdf|
|Word to search|Word to search for in the file name|.fileTest|
|Assign result to variable|Variable where the names of the files will be stored|Variable|

### Get Metadata
  
Obtains file metadata such as: Name, modification date, creation date and file weight.
|Parameters|Description|example|
| --- | --- | --- |
|File path  |Address where the desired files will be searched|C:/User/Usuario/Folder/|
|Select Metadata|Options to get all or a certain metadata|Todos|
|Select unit|Returns the weight of the file in the specified measure|KB, MB or GB|
|Filter by name|Word we want to search for in the file name|.fileTest|
|Filter by extension|Extension that we want to look for in the files|.pdf|
|Assign result to variable|Variable where the found files will be stored|Variable|

### Delete folder contents
  
Deletes all the contents of a folder
|Parameters|Description|example|
| --- | --- | --- |
|File path |Path of the folder from which the content will be deleted|C:/User/Usuario/Folder/|
|Assign result to variable|Variable where the result of the operation will be stored|Variable|

### Copy/Paste folder
  
Copies the folder including all its content
|Parameters|Description|example|
| --- | --- | --- |
|File path to copy |Path of the folder to copy|C:/User/Usuario/Folder/|
|File path to paste |Path of the folder to paste|C:/User/Usuario/Folder/|
|Assign result to variable|Variable where the result of the operation will be stored|Variable|

### Copy/Paste contents
  
Copies the contents of a folder without the root folder
|Parameters|Description|example|
| --- | --- | --- |
|File path to copy |Path of the folder to copy|C:/User/Usuario/Folder/|
|File path to paste |Path of the folder to paste|C:/User/Usuario/Folder/|
|Assign result to variable|Variable where the result of the operation will be stored|Variable|
