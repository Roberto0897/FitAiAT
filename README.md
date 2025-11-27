# 🏋️‍♂️ FitAI - Assistente Fitness Inteligente

> **Trabalho de Conclusão de Curso:** Sistema de treinos personalizado com Inteligência Artificial  
> **Foco:** Arquitetura híbrida Django-Flutter com IA Generativa para personalização de treinos

[![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)

---

## 🎯 Objetivo do Projeto

O **FitAI** é uma plataforma de treinos personalizados que utiliza **Inteligência Artificial Generativa** para oferecer orientação fitness profissional através de recomendações contextualizadas e um chatbot especializado, democratizando o acesso a serviços tradicionalmente restritos por barreiras econômicas.

### Problema Resolvido
- **Falta de personalização** em apps de fitness convencionais
- **Dificuldade de aderência** a programas de exercícios
- **Ausência de orientação inteligente** em tempo real

### Diferenciais Técnicos

 **Zero-Shot Learning**: Personalização imediata sem dependência de dados históricos  
 **Arquitetura Híbrida**: Sistema de fallback garante continuidade mesmo com falhas externas  
 **Privacy by Design**: Segregação de identidade (Firebase) e dados sensíveis (Django)  
 **Chatbot Contextual**: Assistente inteligente e gerador de treinos 

---

## 🏗️ Arquitetura

```
FitAI/
├── fitai_backend/          # Django REST API
│   ├── apps/
│   │   ├── users/          # Autenticação e perfis
│   │   ├── exercises/      # Biblioteca de exercícios  
│   │   ├── workouts/       # Sistema de treinos
│   │   ├── recommendations/# IA de recomendação
│   │   ├── chatbot/        # Chatbot com OpenAI
│   │   └── notifications/  # Sistema de notificações
│   └── core/              # Configurações centrais
│
├── fitai_app/             # Flutter Mobile App
│   ├── lib/
│   │   ├── core/          # Theme, routing, DI
│   │   ├── data/          # Models, repositories  
│   │   ├── domain/        # Entities, use cases
│   │   └── presentation/  # Pages, widgets, BLoC
│   └── test/
│
└── docs/                  # Documentação do TCC
```

---

## 🔧 Tecnologias

### Backend
- **Django 4.2.7** + Django REST Framework
- **PostgreSQL** (produção) / SQLite (desenvolvimento)
- **Google Gemini API** IA Generativa para treinos
- **Token Authentication** para segurança

### Frontend
- **Flutter 3.x** com Material Design 3
- **GoRouter** para navegação declarativa
- **BLoC** para gerenciamento de estado
- **Clean Architecture** para escalabilidade
- **Dio/Retrofit** para comunicação com APIs
- **FlutterSecureStorage**  Armazenamento criptografado

### Infraestrutura e Serviços
- **Firebase Authentication**: Gerenciamento de identidades
- **Git/GitHub**: Controle de versão
- **VS Code**: Ambiente de desenvolvimento
- **Figma**: Prototipagem de interfaces

---

## 📱 Funcionalidades

### 🔐 Autenticação e Perfil
- [x] Cadastro de usuário com Firebase
- [x] Login com email/senha 
- [x] Onboarding com wizard multi-etapas
- [x] Perfil fitness personalizado (objetivos, nível, restrições)
- [x] Sincronização automática Firebase ↔ Django

### 🏋️ Sistema de Treinos
- [x] Catálogo de exercícios com filtros (grupo muscular, equipamento)
- [x] Geração de treinos personalizados via IA
- [x] Visualização detalhada com séries, repetições, carga
- [x] Timer de descanso funcional
- [x] Registro de sessões executadas

### 🤖 Recomendações Inteligentes
- [x] Análise de histórico e padrões de treino
- [x] Identificação de grupos musculares negligenciados
- [x] Recomendações diárias contextualizadas
- [x] Sistema de score de confiança

### 💬 Chatbot Fitness
- [x] Assistente conversacional com Google Gemini
- [x] Contextualização baseada no perfil do usuário
- [x] Entrevista estruturada para geração de treinos
- [x] Respostas em português brasileiro
- [x] Feedback educativo sobre exercícios

### 📊 Dashboard e Métricas
- [x] Visão consolidada do progresso
- [x] Total de treinos realizados
- [x] Card de recomendação inteligente
- [x] Acesso rápido a funcionalidades principais

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- Flutter SDK 3.x
- PostgreSQL (opcional para produção)

### Backend Django

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/fitai-tcc.git
cd fitai-tcc

# Configurar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt


# Executar servidor
python manage.py runserver
```

### Frontend Flutter

```bash
# Navegar para o app Flutter
cd fitai_app

# Instalar dependências
flutter pub get

# Executar aplicativo
flutter run
```

### Variáveis de Ambiente

```env
# .env no fitai_backend/
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost/fitai  # Opcional
```

---

## 📊 APIs Principais

### Autenticação e Usuários
```http
POST /api/v1/users/register/     # Registro de usuário
POST /api/v1/users/login/        # Login
GET  /api/v1/users/dashboard/    # Dashboard personalizado
```

### Sistema de Treinos
```http
GET  /api/v1/workouts/           # Listar treinos
GET  /api/v1/workouts/{id}/      # Detalhes do treino
POST /api/v1/workouts/{id}/start/ # Iniciar sessão
```

### Chatbot Inteligente
```http
POST /api/v1/chat/conversations/start/         # Iniciar conversa
POST /api/v1/chat/conversations/{id}/message/  # Enviar mensagem
GET  /api/v1/chat/conversations/{id}/history/  # Histórico
```

### Recomendações com IA
```http
GET  /api/v1/recommendations/personalized/     # Recomendações do usuário
POST /api/v1/recommendations/ai/generate-workout/ # Gerar treino com IA
```

---

## 🧪 Aspectos Acadêmicos

### 1. Arquitetura Híbrida Validada
- Modelo de integração funcional entre serviços gerenciados (Firebase) e backend próprio (Django)
- Documentação de desafios práticos de sincronização e prevenção de race conditions
- Estratégias de resiliência com fallback determinístico

### 2. Sistema de Recomendação Inovador
- **Zero-Shot Learning** via IA generativa sem dependência de grandes bases históricas
- Combinação de prompts estruturados com regras heurísticas de ciência do exercício
- Transparência algorítmica com justificativas explicativas

### 3. Design Centrado no Contexto de Uso
- Interface otimizada para visualização durante exercícios físicos
- Elementos ampliados e alto contraste para legibilidade em movimento
- Validação por análise heurística baseada nos princípios de Nielsen

### 4. Framework Replicável
- Metodologia documentada para desenvolvimento de aplicações similares em contexto acadêmico
- Transparência sobre limitações e fronteiras de validação
- Modelo de organização de revisão de literatura com identificação explícita de lacunas

---

## 👨‍💻 Autor

Maycon Douglas e Antonio Roberto 
🎓 Tecnologia em Sistemas para internet
📅 TCC 2025

---

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos como parte do Trabalho de Conclusão de Curso.

---

## 🤝 Orientação

**Orientador:** Francisco Euder

---

<div align="center">

**FitAI - Transformando Fitness com Inteligência Artificial**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/seu-usuario)

</div>