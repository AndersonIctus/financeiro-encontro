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
        loadComponent: () => import('./components/lancamentos/lancamentos.component').then(m => m.LancamentosComponent),
      },
      {
        path: 'conciliacao',
        loadComponent: () => import('./components/conciliacao/conciliacao.component').then(m => m.ConciliacaoComponent),
      },
      {
        path: 'arquivos',
        loadComponent: () => import('./components/arquivos/arquivos.component').then(m => m.ArquivosComponent),
      },
    ],
  },
  {
    path: '**',
    loadComponent: () => import('./components/not-found/not-found.component').then(m => m.NotFoundComponent),
  },
];
