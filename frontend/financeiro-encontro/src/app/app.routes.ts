import { Routes } from '@angular/router';
import { authGuard } from './general/auth/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./components/login/login.component').then(m => m.LoginComponent),
  },
  {
    path: '',
    loadComponent: () => import('./components/main/main.component').then(m => m.MainComponent),
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      {
        path: 'dashboard',
        loadComponent: () => import('./components/dashboard/dashboard.component').then(m => m.DashboardComponent),
      },
      {
        path: 'lancamentos',
        children: [
          {
            path: '',
            loadComponent: () => import('./components/lancamentos/lancamentos.component').then(m => m.LancamentosComponent),
          },
          {
            path: 'novo',
            loadComponent: () => import('./components/lancamentos/lancamentos-form/lancamentos-form.component').then(m => m.LancamentosFormComponent),
          },
          {
            path: ':id/editar',
            loadComponent: () => import('./components/lancamentos/lancamentos-form/lancamentos-form.component').then(m => m.LancamentosFormComponent),
          },
        ],
      },
      {
        path: 'conciliacao',
        children: [
          {
            path: '',
            loadComponent: () => import('./components/conciliacao/conciliacao.component').then(m => m.ConciliacaoComponent),
          },
          {
            path: 'conciliar',
            loadComponent: () => import('./components/conciliacao/conciliar-lancamentos/conciliar-lancamentos.component').then(m => m.ConciliarLancamentosComponent),
          },
        ],
      },
      {
        path: 'arquivos',
        loadComponent: () => import('./components/arquivos/arquivos.component').then(m => m.ArquivosComponent),
      },
      {
        path: 'administracao',
        children: [
          {
            path: 'relatorios',
            loadComponent: () => import('./components/administracao/relatorios/relatorios.component').then(m => m.RelatoriosComponent),
          },
          {
            path: 'finalidades',
            children: [
              {
                path: '',
                loadComponent: () => import('./components/administracao/finalidades/finalidades.component').then(m => m.FinalidadesComponent),
              },
              {
                path: 'novo',
                loadComponent: () => import('./components/administracao/finalidades/finalidades-form/finalidades-form.component').then(m => m.FinalidadesFormComponent),
              },
              {
                path: ':id/editar',
                loadComponent: () => import('./components/administracao/finalidades/finalidades-form/finalidades-form.component').then(m => m.FinalidadesFormComponent),
              },
            ],
          },
        ],
      },
    ],
  },
  {
    path: '**',
    loadComponent: () => import('./components/not-found/not-found.component').then(m => m.NotFoundComponent),
  },
];
