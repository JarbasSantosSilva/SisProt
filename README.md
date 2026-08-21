# SisProt

Sistema web para gerenciamento de solicitações e protocolos, desenvolvido com **Python**, **Flask** e **MySQL**.

> **Status:** projeto em desenvolvimento e estudo.

## Sobre o projeto

O SisProt simula um fluxo de atendimento para registro, acompanhamento e tramitação de solicitações. Usuários podem criar uma conta, abrir solicitações e acompanhar seu andamento. Atendentes e administradores possuem funcionalidades específicas para consultar e processar solicitações.

O projeto foi desenvolvido para praticar desenvolvimento web com Flask, autenticação por sessão, controle de acesso por perfil, integração com banco de dados relacional, templates Jinja, JavaScript, testes automatizados e integração contínua.

## Funcionalidades atuais

- Cadastro de usuários solicitantes.
- Login e logout com autenticação por sessão.
- Hash de senhas utilizando Flask-Bcrypt.
- Criação de novas solicitações.
- Consulta das solicitações do usuário autenticado.
- Geração de número de protocolo para cada solicitação.
- Painel de atendimento para usuários com perfil de atendente ou administrador.
- Deferimento e indeferimento de solicitações.
- Registro e consulta do histórico de tramitações.
- Cadastro de atendentes por usuários administradores.
- Listagem e exclusão de atendentes por usuários administradores.
- Endpoint JSON para consulta das solicitações do usuário.
- Endpoint JSON para consulta de protocolo.
- Testes automatizados básicos com Pytest.
- Integração contínua com GitHub Actions.
- Configuração de execução com Gunicorn por meio do `Procfile`.

## Perfis de acesso

| Perfil | Responsabilidades principais |
|---|---|
| `solicitante` | Criar solicitações e acompanhar seus próprios protocolos. |
| `atendente` | Consultar solicitações no painel e realizar tramitações. |
| `admin` | Acessar funções administrativas e gerenciar atendentes. |

## Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal do projeto. |
| Flask | Framework web utilizado na aplicação. |
| Jinja2 | Renderização dos templates HTML. |
| MySQL | Banco de dados relacional. |
| PyMySQL | Conexão da aplicação com o MySQL. |
| Flask-Bcrypt | Geração e validação de hash de senhas. |
| `python-dotenv` | Leitura de variáveis de ambiente. |
| HTML e CSS | Estrutura e apresentação das páginas. |
| JavaScript | Consumo dos endpoints JSON e atualização da interface. |
| Pytest | Testes automatizados. |
| GitHub Actions | Execução automatizada dos testes. |
| Gunicorn | Servidor WSGI para execução da aplicação. |

## Estrutura do projeto

```text
SisProt/
├── .github/
│   └── workflows/
│       └── ci.yml
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── cadastro.js
│       ├── nova_solicitacao.js
│       └── solicitacoes.js
├── templates/
│   ├── base.html
│   ├── cadastro.html
│   ├── cadastro_atendente.html
│   ├── historico.html
│   ├── index.html
│   ├── listar_usuarios.html
│   ├── login.html
│   ├── minhas_solicitacoes.html
│   ├── nova_solicitacao.html
│   └── painel_atendente.html
├── .env.example
├── .gitignore
├── app.py
├── Procfile
├── requirements.txt
└── test_app.py
```

## Pré-requisitos

Antes de executar o projeto, instale:

- Python 3.11 ou superior;
- MySQL Server;
- Git;
- `pip`, gerenciador de pacotes do Python.

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/JarbasSantosSilva/SisProt.git
cd SisProt
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

No Linux ou macOS, ative o ambiente:

```bash
source venv/bin/activate
```

No Windows PowerShell, ative o ambiente:

```powershell
.\venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execução do script apenas nesta sessão, utilize:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração do ambiente

O SisProt utiliza variáveis de ambiente para as credenciais do banco de dados e para a chave secreta da aplicação.

Crie o arquivo `.env` a partir do modelo:

No Linux ou macOS:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Depois, preencha o arquivo `.env` com os dados do seu ambiente:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=sisprot
SECRET_KEY=troque_esta_chave
```

> Nunca publique o arquivo `.env` real no GitHub. O arquivo `.env.example` deve conter apenas nomes de variáveis e valores fictícios.

## Banco de dados

Crie um banco de dados MySQL com o mesmo nome definido na variável `DB_NAME` do arquivo `.env`.

A aplicação utiliza tabelas relacionadas às seguintes entidades:

| Entidade | Finalidade |
|---|---|
| `usuarios` | Usuários, credenciais e perfis de acesso. |
| `tipos_solicitacao` | Tipos disponíveis para abertura de solicitações. |
| `solicitacoes` | Solicitações abertas pelos usuários. |
| `tramitacoes` | Histórico de alterações e decisões sobre as solicitações. |

> **Limitação atual:** o repositório ainda não inclui um script SQL ou migração para criar automaticamente as tabelas. A estrutura inicial do banco precisa ser preparada manualmente antes da execução completa do fluxo.

## Execução local

Com o ambiente virtual ativado, o `.env` configurado e o MySQL em execução, inicie a aplicação com:

```bash
python app.py
```

A aplicação será disponibilizada localmente em:

```text
http://127.0.0.1:5000
```

Para execução com Gunicorn, o arquivo `Procfile` utiliza:

```text
web: gunicorn app:app
```

## Principais rotas

| Rota | Método | Acesso | Finalidade |
|---|---|---|---|
| `/` | `GET` | Público | Página inicial. |
| `/cadastro` | `GET`, `POST` | Público | Cadastro de usuário solicitante. |
| `/login` | `GET`, `POST` | Público | Autenticação do usuário. |
| `/logout` | `GET` | Autenticado | Encerramento da sessão. |
| `/nova_solicitacao` | `GET`, `POST` | Autenticado | Criação de solicitação. |
| `/minhas_solicitacoes` | `GET` | Autenticado | Consulta das solicitações do usuário. |
| `/painel_atendente` | `GET` | Atendente/Admin | Painel de atendimento. |
| `/deferir/<id>` | `GET` | Atendente/Admin | Deferimento de solicitação. |
| `/indeferir/<id>` | `GET` | Atendente/Admin | Indeferimento de solicitação. |
| `/historico/<id>` | `GET` | Autenticado | Consulta do histórico de uma solicitação. |
| `/cadastro_atendente` | `GET`, `POST` | Admin | Cadastro de atendente. |
| `/listar_usuarios` | `GET` | Admin | Listagem de atendentes. |
| `/excluir_usuario/<id>` | `GET` | Admin | Exclusão de atendente. |
| `/api/solicitacoes` | `GET` | Autenticado | Retorno das solicitações em JSON. |
| `/api/protocolo/<numero>` | `GET` | Conforme regra atual | Consulta de protocolo em JSON. |

## Fluxo principal

O fluxo básico da aplicação é:

```text
1. Usuário cria uma conta.
2. Usuário realiza login.
3. Usuário abre uma solicitação.
4. Sistema gera um número de protocolo.
5. Usuário acompanha a solicitação.
6. Atendente consulta o painel.
7. Atendente defere ou indefere a solicitação.
8. Sistema registra a tramitação no histórico.
```

## Testes

Execute os testes automatizados com:

```bash
pytest test_app.py -v
```

Os testes atuais verificam a página inicial, as páginas de login e cadastro e o redirecionamento de uma rota protegida quando não há usuário autenticado.

## Integração contínua

O workflow do GitHub Actions é executado em `push` e `pull request` para a branch `main`. O processo configura o Python, instala as dependências e executa os testes automatizados.

O workflow pode ser consultado em:

```text
.github/workflows/ci.yml
```

## Segurança e limitações atuais

O projeto já utiliza hash de senhas e controle de acesso por sessão. Entretanto, ainda está em evolução.

As próximas melhorias recomendadas são:

- Adicionar proteção CSRF aos formulários.
- Revisar a autorização da consulta de protocolos e históricos.
- Evitar operações que alteram dados utilizando requisições `GET`.
- Adicionar script SQL ou migrações do banco.
- Ampliar a cobertura de testes de autenticação, autorização e tramitação.
- Separar rotas, regras de negócio e acesso ao banco em módulos menores.
- Padronizar o tratamento de erros.
- Configurar uma versão de produção com variáveis e permissões adequadas.

## Objetivo de aprendizagem

O SisProt faz parte da minha jornada de desenvolvimento backend. Por meio dele, estou praticando Python, Flask, MySQL, autenticação por sessão, controle de acesso por perfil, integração com banco de dados, templates Jinja, JavaScript, testes automatizados e integração contínua.

## Autor

**Jarbas Santos Silva**

- GitHub: [github.com/JarbasSantosSilva](https://github.com/JarbasSantosSilva)
- LinkedIn: [linkedin.com/in/jarbassantossilva](https://www.linkedin.com/in/jarbassantossilva/)
