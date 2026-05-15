



# Arquivos
  
Gerencie seus arquivos e pastas, abra e leia arquivos, controle sua existência e obtenha seus metadados.  

*Read this in other languages: [English](Manual_Files.md), [Português](Manual_Files.pr.md), [Español](Manual_Files.es.md)*
  
![banner](imgs/Banner_Files.png)
## Como instalar este módulo
  
Para instalar o módulo no Rocketbot Studio, pode ser feito de duas formas:
1. Manual: __Baixe__ o arquivo .zip e descompacte-o na pasta módulos. O nome da pasta deve ser o mesmo do módulo e dentro dela devem ter os seguintes arquivos e pastas: \__init__.py, package.json, docs, example e libs. Se você tiver o aplicativo aberto, atualize seu navegador para poder usar o novo módulo.
2. Automático: Ao entrar no Rocketbot Studio na margem direita você encontrará a seção **Addons**, selecione **Install Mods**, procure o módulo desejado e aperte instalar.  



# Como usar este módulo



## Descrição do comando

### Abrir Pasta
  
Abra a pasta que contém um arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta|Abra o tapete de rota especificado|C:/User/Usuario/Pasta/|
|Asignar resultado a variable|Variável onde o resultado será armazenado|Variável|

### Abrir Arquivo
  
Abre um arquivo 
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção do arquivo|Abra o arquivo do direção especificado|C:/User/Usuario/Folder/File.extension|
|Asignar resultado a variable|Variável onde o resultado será armazenado|Variável|

### Selecione o arquivo
  
Peça ao usuário para selecionar um arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Nome da variável onde salvar o caminho|Ao executá-lo, o explorador de arquivos se abre para que possamos selecionar o arquivo, uma vez selecionado, ele nos fornece o endereço onde está localizado.|Result|

### Selecionar Pasta
  
Peça ao usuário para selecionar uma pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Nome da variável onde salvar o caminho|Quando executado, o explorador de arquivos abre para que possamos selecionar a pasta que desejamos, uma vez selecionada, retorna o caminho onde está localizada|Result|

### Renomear pasta
  
Pede ao usuário para selecionar uma pasta para renomear
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta a cambiar |Ao executar, a pasta que especificamos é renomeada|C:/User/Folder/|
|Nuevo nome da pasta|Nome da pasta sem o caminho|Nuevo nome|
|Asignar resultado a variable|Variável onde o resultado será armazenado|Variável|

### Ler arquivo
  
Ler um arquivo de texto simples e salva seu conteúdo em uma variável
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção do arquivo|Direção do arquivo a ler|C:/Users/User/Desktop/file.txt|
|Codificação|Codificação do arquivo a ler. Ex latin-1, utf-8, etc|latin-1|
|Separar cada linha|Retorna o conteúdo de um arquivo e armazena em uma variável, se a opção linhas separadas estiver marcada, retorna o conteúdo do arquivo dentro de uma lista e cada linha é um elemento dentro da lista|True|
|Atribuir resultado à variável|Variável onde o valor obtido será armazenado|Variável|

### Elimina una carpeta
  
Excluir uma pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta|Seleciona a direção da pasta que deseja remover|C:/User/Usuario/Folder/|
|Asignar resultado a variable|Variável onde o resultado será armazenado|Variável|

### Excluir um arquivo
  
Excluir um arquivo indicando sua extensão e seu nome ou parte do nome
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta|Direção do arquivo a ser removido|C:/User/Usuario/Folder/|
|Tipo do arquivo a eliminar|Nome e extension do arquivo a ser removido|nome*.pdf|
|Asignar resultado a variable|Variável onde o resultado será armazenado|Variável|

### Criar Pasta
  
Digite a direção e o nome onde você deseja criar a pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção e nome da pasta|Direção onde se creara à pasta|C:/Users/User/Desktop/folder_test|
|Asignar resultado a variable|Variável onde o resultado será armazenado|Variável|

### Provar a existência
  
Verifique se existe um arquivo ou pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta|Direção da pasta que você deseja verificar a existência|C:/User/Usuario/Folder/|
|Asignar resultado a variable|Variável onde o resultado será armazenado|Variável|

### Listar arquivos ordenados
  
Listar archivos y selecciona el orden
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta|Direção da pasta da qual se deseja listar os arquivos|C:/User/Usuario/Folder/|
|Organizar por|Opções para encomendar, Nome, Data e Tipo|Name|
|Atribuir resultado à variável|Variável onde a lista de itens da pasta está armazenada|Variável|

### Achar arquivo
  
Retorna uma lista com correspondências
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta|Direção onde o arquivo será pesquisado|C:/User/Usuario/Folder/|
|Filtrar por extensão|Filtre por extensão procurando todos os arquivos com a extensão especificada|.pdf|
|Palavra a procurar|Palavra a procurar no nome do arquivo|.fileTest|
|Atribuir resultado à variável|Variable donde se almacenan los nombres de los archivos|Variável|

### Obter metadados
  
Obtém metadados do arquivo como: Nome, data de modificação, data de criação e peso do arquivo.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção de arquivo |Direção onde os arquivos desejados serão pesquisados|C:/User/Usuario/Folder/|
|Selecionar metadados|Opções para obter todos ou um determinado metadados|Todos|
|Selecionar unidade|Retorna o peso do arquivo na medida especificada|KB, MB o GB|
|Filtrar por nome|Palavra que queremos pesquisar no nome do arquivo|.fileTest|
|Filtrar por extensão|Extensão que queremos procurar nos arquivos|.pdf|
|Atribuir resultado à variável|Variável onde os arquivos encontrados são armazenados|Variável|

### Excluir conteúdo da pasta
  
Exclui todo o conteúdo de uma pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta|Caminho da pasta do qual o conteúdo será excluído|C:/User/Usuario/Folder/|
|Atribuir resultado à variável|Variável onde o resultado da operação será armazenado|Variável|

### Copiar/Pegar pasta
  
Copia toda ou o conteúdo de uma pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta a ser copiada |Direção da pasta a ser copiada|C:/User/Usuario/Folder/|
|Direção da pasta a ser colada |Direção da pasta a ser colada|C:/User/Usuario/Folder/|
|Atribuir resultado à variável|Variável onde o resultado da operação será armazenado|Variável|

### Copiar/Pegar conteúdo
  
Copia todo o conteúdo de uma pasta sem a pasta raíz
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Direção da pasta a ser copiada |Direção da pasta a ser copiada|C:/User/Usuario/Folder/|
|Direção da pasta a ser colada |Direção da pasta a ser colada|C:/User/Usuario/Folder/|
|Atribuir resultado à variável|Variável onde o resultado da operação será armazenado|Variável|
