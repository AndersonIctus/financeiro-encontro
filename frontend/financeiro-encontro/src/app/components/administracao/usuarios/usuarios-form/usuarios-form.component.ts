import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import {
  MaterialGlobalModule,
  MaterialFormsModule,
} from '../../../../shared/modules/material.imports.module';
import { ToastService }      from '../../../../shared/components/toast/toast.service';
import { ErrorHandlerService } from '../../../../shared/services/error-handler.service';
import { UsuarioService }    from '../../../../services/usuario.service';

@Component({
  selector: 'app-usuarios-form',
  standalone: true,
  imports: [CommonModule, MaterialGlobalModule, MaterialFormsModule],
  templateUrl: './usuarios-form.component.html',
  styleUrl: './usuarios-form.component.scss',
})
export class UsuariosFormComponent implements OnInit {
  private fb             = inject(FormBuilder);
  private route          = inject(ActivatedRoute);
  private router         = inject(Router);
  private usuarioService = inject(UsuarioService);
  private toast          = inject(ToastService);
  private errorHandler   = inject(ErrorHandlerService);

  form!: FormGroup;
  saving     = false;
  loading    = false;
  updatePage = false;
  usuarioId: number | null = null;
  senhaVisivel = false;

  ngOnInit(): void {
    this.form = this.fb.group({
      nome:  ['', [Validators.required, Validators.maxLength(100)]],
      email: ['', [Validators.required, Validators.email]],
      senha: ['', Validators.required],
      ativo: [true],
    });

    const id = this.route.snapshot.params['id'];
    if (id) {
      this.updatePage = true;
      this.usuarioId  = Number(id);
      this.form.get('senha')!.clearValidators();
      this.form.get('senha')!.updateValueAndValidity();
      this.loadValues(this.usuarioId);
    }
  }

  private loadValues(id: number): void {
    this.loading = true;
    this.usuarioService.buscarPorId(id).subscribe({
      next: (data) => {
        this.form.patchValue({ nome: data.nome, email: data.email, ativo: data.ativo });
        this.loading = false;
      },
      error: (err) => {
        this.errorHandler.handler(err);
        this.loading = false;
        this.voltar();
      },
    });
  }

  voltar(): void {
    this.router.navigate(['/administracao/usuarios']);
  }

  salvar(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.toast.warning({ message: 'Preencha todos os campos obrigatórios.' });
      return;
    }

    const { nome, email, senha, ativo } = this.form.value;
    this.saving = true;

    const req$ = this.updatePage && this.usuarioId
      ? this.usuarioService.editar(this.usuarioId, { nome, email, ativo, ...(senha ? { senha } : {}) })
      : this.usuarioService.criar({ nome, email, senha, ativo });

    const msg = this.updatePage ? 'Usuário atualizado com sucesso.' : 'Usuário criado com sucesso.';

    req$.subscribe({
      next: () => {
        this.toast.success({ message: msg });
        this.saving = false;
        this.voltar();
      },
      error: (err) => {
        this.errorHandler.handler(err);
        this.saving = false;
      },
    });
  }
}
