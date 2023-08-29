# loan-analysis
Este projeto é um site simples de análise de empréstimo.
Ele possui um formulário que pode ser editado pela página de administração.
Ao fazer o envio do formulário é feito uma pré-análise dos dados por meio de uma API externa e caso seja pré-aprovado um administrador pode aprovar ou reprovar o empréstimo pela página de administração.

## Instalação
Para rodar o projeto é necessário possuir o [Docker](https://docs.docker.com/desktop/install/windows-install/) e docker-compose instalados.

Na pasta raiz do projeto execute o comando:
```bash
docker-compose up -d
```

## Uso
Para acessar o site basta acessar o endereço: http://localhost
Para acessar a página de administração basta acessar o endereço: http://localhost:8000/admin

O usuário e senha padrão são:
```
Usuário: admin
Senha: admin
```