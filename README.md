# Finance Diary 🐍💰

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-brightgreen.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.14-red.svg)

Sistema de gerenciamento financeiro pessoal com API RESTful e futura integração mobile.

## 📂 Estrutura do Projeto

```
finance_diary/
├── core/ # Configurações principais
│ ├── settings/ # Ambiente dividido
│ │ ├── base.py # Configs base
│ │ ├── development.py # Configs desenvolvimento
│ │ └── production.py # Configs produção
│ └── urls.py # Rotas principais
│
├── apps/
│ ├── users/ # Gerenciamento de usuários
│ │ ├── models.py # Modelo User customizado
│ │ └── serializers.py # Serializers para API
│ │
│ └── transactions/ # Módulo de transações
│ ├── models/ # Models divididos
│ ├── services/ # Lógica de negócio
│ └── tests/ # Testes unitários
│
├── static/ # Arquivos estáticos
├── templates/ # Templates frontend
├── requirements/ # Requirements divididos
│ ├── base.txt # Dependências principais
│ ├── dev.txt # Dev-only
│ └── prod.txt # Produção
│
└── manage.py # CLI Django
```

## 🛠️ Configuração do Ambiente

### Pré-requisitos
- Python 3.10+
- PostgreSQL 14+
- Poetry (gerenciamento de dependências)

### Instalação
```
# Clone o repositório
git clone -b feature/config_inicial https://github.com/luc4sm0ur4/finance_diary.git
cd finance_diary


# Configure o ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver


```

🤝 Como Contribuir
------------------

1.  Faça fork do projeto
    
2.  Crie uma branch (git checkout -b feature/nova-feature)
    
3.  Commit suas mudanças (git commit -m 'Adiciona nova feature')
    
4.  Push para a branch (git push origin feature/nova-feature)
    
5.  Abra um Pull Request
    

📄 Licença
----------

GPL-3.0 License - Veja [LICENSE]([https://LICENSE](https://www.gnu.org/licenses/gpl-3.0.html)) para detalhes.

✉️ Contato
----------

Lucas Moura - [@luc4sm0ur4](https://github.com/luc4sm0ur4)
