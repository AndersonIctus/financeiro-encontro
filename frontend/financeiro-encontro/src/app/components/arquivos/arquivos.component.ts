import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-arquivos',
  standalone: true,
  imports: [MatIconModule],
  template: `
    <div class="coming-soon">
      <mat-icon>folder_open</mat-icon>
      <h2>Arquivos Enviados</h2>
      <p>Em breve implementado</p>
    </div>
  `,
  styles: [`
    .coming-soon {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      min-height: 400px;
      gap: 12px;
      color: var(--mat-sys-on-surface-variant);

      mat-icon { font-size: 64px; width: 64px; height: 64px; opacity: 0.4; }
      h2 { margin: 0; font-size: 1.5rem; font-weight: 500; }
      p  { margin: 0; font-size: 1rem; opacity: 0.7; }
    }
  `],
})
export class ArquivosComponent {}
