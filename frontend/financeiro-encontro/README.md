# Financeiro Encontro — Frontend

Frontend do sistema **Financeiro Encontro**, interface web para gerenciamento financeiro de eventos da igreja.

---

## Tecnologias

- Angular 21 (standalone components)
- TypeScript 5.9 (strict mode)
- SCSS
- Chart.js 4 + ng2-charts (gráficos do dashboard)
- Moment.js
- Vitest

---

## Pré-requisitos

O backend deve estar rodando antes de iniciar o frontend.
Veja as instruções em [backend/README.md](../../backend/README.md).

---

## Como rodar

```bash
npm install
npm start        # ng serve em http://localhost:4200
```

---

## Comandos disponíveis

| Comando | Descrição |
|---|---|
| `npm start` | Servidor de desenvolvimento em `:4200` |
| `npm run build` | Build de produção em `dist/` |
| `npm test` | Testes unitários com Vitest |
| `npm run test:watch` | Testes em modo watch (Vitest) |

---

## Estrutura do projeto

```
src/
├── environments/
│   ├── environment.ts          # API_URL desenvolvimento
│   └── environment.prod.ts     # API_URL produção
├── app/
│   ├── models/                 # Interfaces TypeScript (espelham o backend)
│   ├── services/               # Serviços HTTP (extendem AbstractService)
│   │   ├── abstract.service.ts # Base genérica com paginação e filtros
│   │   ├── auth.service.ts
│   │   ├── lancamento.service.ts
│   │   ├── finalidade.service.ts
│   │   ├── extrato-bancario.service.ts
│   │   ├── conciliacao.service.ts
│   │   ├── dashboard.service.ts
│   │   ├── dashboard-state.service.ts  # Estado compartilhado do dashboard
│   │   ├── dto/                # DTOs de filtro para cada endpoint
│   │   └── util/               # Utilitários (PageTemplate)
│   ├── general/
│   │   └── auth/               # Auth interceptor e guard JWT
│   └── components/             # Componentes por tela (lazy loaded)
│       ├── login/
│       ├── main/               # Shell principal com navegação lateral
│       ├── dashboard/
│       │   └── graphs/         # Gráficos Chart.js
│       │       ├── barra-mensal/
│       │       ├── barra-top-finalidades/
│       │       └── pizza-finalidade/
│       │           └── lista-lancamentos-graph/
│       ├── lancamentos/
│       │   └── lancamentos-form/
│       ├── conciliacao/
│       │   ├── conciliacao-upload-dialog/
│       │   └── conciliar-lancamentos/
│       │       └── conciliacao-card/
│       ├── arquivos/           # Listagem de extratos importados
│       ├── administracao/
│       │   └── finalidades/
│       │       └── finalidades-form/
│       └── not-found/
└── styles.scss                 # Estilos globais
```

---

## Autenticação

O login é feito via `POST /auth/login`. O token JWT retornado é salvo no `localStorage` e injetado automaticamente em todas as requisições pelo `authInterceptor`. Rotas protegidas usam o `authGuard`.

---

## Variáveis de ambiente

### Desenvolvimento local

O Angular usa `src/environments/environment.ts` automaticamente com `npm start`. Edite o arquivo para apontar para o backend correto:

```typescript
export const environment = {
  production: false,
  API_URL: 'http://localhost:8000'
};
```

### Produção (build)

O `ng build` troca automaticamente `environment.ts` por `environment.prod.ts` (configurado via `fileReplacements` no `angular.json`).

Os valores de `environment` são **compilados dentro do bundle** em tempo de build — não é possível alterá-los depois sem recompilar.

### Deploy em nuvem (Docker)

Passe a URL do backend como build arg:

```bash
docker build --build-arg API_URL=https://api.seudominio.com -t financeiro-frontend .
```

Se omitido, o valor padrão é `http://localhost:8000`.

> O Dockerfile substitui o placeholder `##API_URL##` em `environment.prod.ts` antes de compilar o Angular.
