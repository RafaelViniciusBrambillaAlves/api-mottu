# 🏍️ Motorcycle Rental API

![Python](https://img.shields.io/badge/Python-3.9-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Kafka](https://img.shields.io/badge/Kafka-Messaging-black)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Sobre o projeto

Este projeto foi desenvolvido como **estudo prático baseado no desafio backend da Mottu** ([repositório oficial do desafio](https://github.com/Mottu-ops/Desafio-BackEnd)). O objetivo foi criar uma API backend robusta para **gerenciamento de motos, entregadores e locações**, aplicando boas práticas de arquitetura, mensageria, modelagem de dados e infraestrutura com Docker.

> ⚠️ Observação: apesar do desafio original solicitar .NET/C#, este projeto foi implementado em **Python (FastAPI)** apenas como exercício técnico e arquitetural.

---

## 🎯 Objetivo do desafio

Criar uma aplicação backend capaz de:

* Gerenciar motos (CRUD)
* Gerenciar entregadores
* Permitir locação de motos com regras de negócio bem definidas
* Publicar eventos via mensageria quando uma moto for cadastrada
* Consumir eventos específicos (motos do ano 2024)
* Persistir notificações no banco para consulta futura

---

## 🧠 O que foi implementado

### ✅ Funcionalidades principais

#### 🏍️ Motos

* Cadastro de motos (modelo, ano, VIN)
* Validação de VIN único
* Listagem e consulta por ID
* Atualização de placa/VIN
* Remoção condicionada à inexistência de locações
* **Publicação de evento Kafka (`motorcycle.created`) ao cadastrar**

#### 📩 Mensageria (Kafka)

* Producer Kafka para eventos de criação de moto
* Consumer Kafka escutando o tópico `motorcycle.created`
* Filtro para motos do ano **2024**
* Persistência da notificação no banco (`motorcycle_notifications`)

#### 👤 Entregadores

* Cadastro de usuários entregadores
* Validação de CNH (A, B ou A+B)
* Upload da foto da CNH
* Armazenamento da imagem fora do banco (MinIO)

#### 📝 Locações

* Planos de locação configuráveis via banco
* Validação de datas de início e término
* Regra de habilitação (CNH A obrigatória)
* Cálculo automático do valor total
* Multas por devolução antecipada
* Acréscimos por devolução atrasada

---

## 🏗️ Arquitetura do projeto

### 🔁 Diagrama de arquitetura (simplificado)

```
Client (HTTP)
   │
   ▼
FastAPI (Routes)
   │
   ▼
Services (Business Rules)
   │
   ▼
Repositories
   │
   ▼
PostgreSQL

FastAPI
   │
   ├──► Kafka Producer ──► Topic: motorcycle.created
   │                          │
   │                          ▼
   │                   Kafka Consumer
   │                          │
   │                          ▼
   │              motorcycle_notifications (PostgreSQL)
   │
   └──► MinIO (CNH images)
```

O diagrama acima representa o fluxo principal da aplicação, incluindo requisições HTTP, persistência de dados, mensageria assíncrona e armazenamento de arquivos.

O projeto segue uma arquitetura em camadas, separando responsabilidades:

* **API / Routes**: definição das rotas HTTP
* **Services**: regras de negócio
* **Repositories**: acesso a dados
* **Models**: entidades do banco (SQLAlchemy)
* **Schemas**: contratos de entrada/saída (Pydantic)
* **Messaging**: Kafka consumer e handlers
* **Core**: configurações, autenticação, logging, Kafka, MinIO

---

## 📂 Estrutura de pastas

```
|_ alembic
|_ app
│   |_ api
│   │   |_ routes
│   │       |_ admin.py
│   │       |_ auth.py
│   │       |_ motorcycles.py
│   │       |_ rentals.py
│   │       |_ users.py
│   │   |_ deps.py
│   |_ core
│   │   |_ auth.py
│   │   |_ exceptions.py
│   │   |_ exception_handlers.py
│   │   |_ jwt.py
│   │   |_ security.py
│   │   |_ kafka.py
│   │   |_ kafka_admin.py
│   │   |_ logging.py
│   │   |_ minio.py
│   │   |_ startup.py
│   │   |_ config.py
│   |_ events
│   │   |_ motorcycle_events.py
│   |_ messaging
│   │   |_ consumer.py
│   │   |_ handlers.py
│   |_ models
│   │   |_ motorcycle.py
│   │   |_ motorcycle_notifications.py
│   │   |_ rental.py
│   │   |_ rental_plan.py
│   │   |_ user.py
│   |_ repositories
│   |_ schemas
│   |_ services
│   |_ scripts
│   │   |_ seed_rental_plans.py
│   |_ database.py
│   |_ main.py
|_ docker-compose.yml
|_ Dockerfile
|_ requirements.txt
|_ alembic.ini
```

---

## 🛠️ Tecnologias utilizadas

* **Python 3.9**
* **FastAPI**
* **SQLAlchemy + Alembic**
* **PostgreSQL**
* **Kafka + Zookeeper**
* **MinIO (storage de imagens)**
* **Docker & Docker Compose**

---

## 🔧 Variáveis de ambiente

As variáveis abaixo são obrigatórias para o funcionamento da aplicação e estão centralizadas no arquivo `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/app_db

SECRET_KEY=your-secret-key

JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7

MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123
MINIO_BUCKET=storage-photos
MINIO_SECURE=False

KAFKA_BOOTSTRAP_SERVERS=kafka:29092
KAFKA_MOTORCYCLE_TOPIC=motorcycle.created
KAFKA_CONSUMER_GROUP=motorcycle-notification-service
```

> ⚠️ **Importante**: nunca versionar o arquivo `.env` em repositórios públicos.

---

## ▶️ Como rodar o projeto

### 1️⃣ Subir os containers

```bash
docker compose up -d
```

### 2️⃣ Rodar as migrations

```bash
docker-compose exec api alembic revision --autogenerate -m "initial"
docker-compose exec api alembic upgrade head
```

### 3️⃣ Seed dos planos de locação

```bash
docker-compose exec api python app/scripts/seed_rental_plans.py
```

### 4️⃣ Acessar a API

* API: [http://localhost:80](http://localhost:80)
* Swagger: [http://localhost:80/docs](http://localhost:80/docs)

---

## 🔐 Usuário admin padrão

Ao iniciar a aplicação, um usuário admin padrão é criado automaticamente:

```
Email: admin@admin.com
Senha: admin123
```

Esse usuário pode ser utilizado para testar os fluxos administrativos.

---

## 📡 Kafka – comandos úteis

Entrar no container do Kafka:

```bash
docker exec -it kafka bash
```

Listar tópicos:

```bash
kafka-topics --bootstrap-server localhost:9092 --list
```

Consumir mensagens:

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic motorcycle.created --from-beginning
```

---

## 📜 Logs da aplicação

```bash
docker logs fastapi-api-1 -f
```

---

## 🚀 Considerações finais

Este projeto foi desenvolvido com foco em:

* Código limpo
* Separação de responsabilidades
* Regras de negócio bem definidas
* Infraestrutura reproduzível
* Mensageria assíncrona

Apesar de ir além do escopo mínimo do desafio (ex: autenticação), o objetivo foi demonstrar **maturidade técnica e boas práticas de backend**.

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Sinta-se livre para usar, estudar e adaptar.

---

👨‍💻 Desenvolvido para fins de estudo e evolução técnica.
