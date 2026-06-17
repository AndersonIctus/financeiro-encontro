import {
  ChangeDetectorRef,
  Component,
  inject,
  OnInit,
  AfterViewInit,
  ViewEncapsulation,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { PageEvent } from '@angular/material/paginator';

import { MaterialGlobalModule } from '../../../shared/modules/material.imports.module';
import { ConfirmDialogComponent } from '../../../shared/components/confirm-dialog/confirm-dialog.component';
import { ToastService }    from '../../../shared/components/toast/toast.service';
import { AuthService }     from '../../../services/auth.service';
import { UsuarioService }  from '../../../services/usuario.service';
import { Usuario }         from '../../../models/usuario.model';
import { PageTemplate }    from '../../../services/util/PageTemplate';

const ADMIN_ID = 1;

@Component({
  selector: 'app-usuarios',
  standalone: true,
  encapsulation: ViewEncapsulation.None,
  imports: [CommonModule, MaterialGlobalModule],
  templateUrl: './usuarios.component.html',
  styleUrl: './usuarios.component.scss',
})
export class UsuariosComponent implements OnInit, AfterViewInit {
  private usuarioService = inject(UsuarioService);
  private authService    = inject(AuthService);
  private router         = inject(Router);
  private dialog         = inject(MatDialog);
  private toast          = inject(ToastService);
  private cdr            = inject(ChangeDetectorRef);

  result: PageTemplate<Usuario> = new PageTemplate<Usuario>();
  loading   = false;
  pageIndex = 0;
  pageSize  = 10;

  currentUserId = this.authService.getUsuario()?.id ?? -1;

  displayedColumns = ['nome', 'email', 'status', 'acoes'];

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    setTimeout(() => this.load());
  }

  load(): void {
    this.loading = true;
    this.usuarioService
      .list({ skip: this.pageIndex * this.pageSize, limit: this.pageSize })
      .subscribe({
        next: (data) => {
          this.result  = data;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: () => {
          this.loading = false;
          this.cdr.detectChanges();
        },
      });
  }

  onPage(event: PageEvent): void {
    this.pageIndex = event.pageIndex;
    this.pageSize  = event.pageSize;
    this.load();
  }

  criar(): void  { this.router.navigate(['/administracao/usuarios/novo']); }
  editar(id: number): void { this.router.navigate(['/administracao/usuarios', id, 'editar']); }

  podeDeletar(usuario: Usuario): boolean {
    return usuario.id !== ADMIN_ID && usuario.id !== this.currentUserId;
  }

  deletar(usuario: Usuario): void {
    this.dialog.open(ConfirmDialogComponent, {
      width: '420px',
      data: {
        title:   'Confirmar exclusão',
        message: `Deseja excluir o usuário "${usuario.nome}"? Esta ação não pode ser desfeita.`,
      },
    }).afterClosed().subscribe((ok: boolean) => {
      if (!ok) return;
      this.usuarioService.remover(usuario.id).subscribe({
        next: () => {
          this.toast.success({ message: 'Usuário excluído com sucesso.' });
          if (this.result.items.length === 1 && this.pageIndex > 0) this.pageIndex--;
          this.load();
        },
        error: (err) => this.toast.error({ message: err?.error?.detail ?? 'Erro ao excluir usuário.' }),
      });
    });
  }
}
