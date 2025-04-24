**Backup de Usuários**

O Backup de Usuários é um aplicativo para Windows que facilita a realização de backups das pastas de usuários localizadas em C:\Users. Ele permite selecionar usuários, escolher uma unidade de armazenamento externa, e copiar as pastas selecionadas para uma pasta de backup com a data atual. O aplicativo possui uma interface gráfica amigável com uma animação divertida (semelhante ao jogo do dinossauro do Google Chrome) durante o processo de backup.
Funcionalidades

Listagem e seleção de usuários em C:\Users com checkboxes.
Seleção de unidade externa para o backup.
Criação de uma pasta de backup com a data atual (ex.: Backup_2025-04-24_15-30-00).
Animação de um dinossauro pulando obstáculos durante o backup.
Barra de progresso para acompanhar o andamento.
Confirmação ao cancelar o backup.

Requisitos

Sistema operacional: Windows.
Permissões de administrador (necessárias para acessar pastas de usuários).
Para desenvolvimento: Python 3.6+ e dependências listadas abaixo.

Instalação (Para Desenvolvedores)

Clone ou baixe o projeto:

Certifique-se de ter o arquivo backup_app.py.


Instale as dependências:

Abra um terminal e instale as bibliotecas necessárias:pip install pyqt5 psutil pyinstaller




Execute o aplicativo:

No terminal, navegue até o diretório do projeto e execute:python backup_app.py





Como Usar

Inicie o aplicativo:

Execute o backup_app.exe (ou o script Python, se estiver em modo de desenvolvimento).
Recomenda-se executar como administrador (clique com o botão direito no .exe e selecione "Executar como administrador").


Selecione os usuários:

Na primeira tela, marque os usuários que deseja incluir no backup.
Clique em "Avançar".


Selecione a unidade de destino:

Escolha uma unidade externa (ex.: HD externo ou pen drive) na lista.
Clique em "Iniciar Backup".


Acompanhe o progresso:

Durante o backup, você verá uma animação de um dinossauro pulando cactos e uma barra de progresso.
Para cancelar, clique em "Cancelar" e confirme a ação.


Conclusão:

Ao finalizar, uma mensagem de sucesso será exibida, e o backup estará na unidade selecionada, dentro de uma pasta com a data do backup.



Como Empacotar em .exe
Para criar um executável .exe e distribuí-lo sem a necessidade de instalar Python:

Instale o PyInstaller (se ainda não instalou):
pip install pyinstaller


Navegue até o diretório do projeto:
cd caminho/para/seu/projeto


Execute o comando do PyInstaller:
pyinstaller --onefile --windowed backup_app.py


--onefile: Gera um único arquivo .exe.
--windowed: Evita a exibição de uma janela de console.


Localize o .exe:

O arquivo backup_app.exe estará na pasta dist.


Teste o .exe:

Execute o backup_app.exe como administrador para garantir acesso às pastas de usuários.



Opcional: Adicionar um Ícone
Para personalizar o ícone do .exe:
pyinstaller --onefile --windowed --icon=caminho/para/seu_icone.ico backup_app.py


O ícone deve estar no formato .ico.

Notas

Permissões: O aplicativo precisa de permissões administrativas para acessar pastas em C:\Users. Sempre execute como administrador.
Tamanho do .exe: O executável pode ser grande (50-100 MB) devido às dependências do PyQt5.
Compatibilidade: Funciona apenas em Windows. Testado em versões 64-bit, mas deve ser compatível com 32-bit.
Melhorias Futuras:
Adicionar sprites personalizados para o dinossauro e obstáculos.
Incluir opção de compactação do backup (ex.: .zip).
Adicionar suporte a subpastas específicas (ex.: apenas Documents ou Desktop).



Licença
Este projeto é de uso livre para fins educacionais e pessoais. Para uso comercial, entre em contato com o autor.
Autor
Desenvolvido com ❤️ por Murilo Martins.
