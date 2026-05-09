import { Component, inject, OnInit }          from '@angular/core';
import { CommonModule, CurrencyPipe, DatePipe } from '@angular/common';
import { FormBuilder, FormGroup }               from '@angular/forms';
import { Router }                               from '@angular/router';
import { MatDialog }                            from '@angular/material/dialog';
import { PageEvent }                            from '@angular/material/paginator';
import moment                                   from 'moment';

import {
  MaterialGlobalModule,
  MaterialFormsModule,
  MaterialDatepickerModule,
} from '../../shared/modules/material.imports.module';
import { ConfirmDialogComponent } from '../../shared/components/confirm-dialog/confirm-dialog.component';
import { ToastService }           from '../../shared/components/toast/toast.service';
import { LancamentoService }      from '../../services/lancamento.service';
import { FinalidadeService }      from '../../services/finalidade.service';
import { Lancamento }             from '../../models/lancamento.model';
import { Finalidade }             from '../../models/finalidade.model';
import { PageTemplate }           from '../../services/util/PageTemplate';
import { TipoLancamento }         from '../../models/constants/tipo-lancamento';
import { StatusLancamento }       from '../../models/constants/status-lancamento';
import { FormaPagamento }         from '../../models/constants/forma-pagamento';

@Component({
  selector: 'app-lancamentos',
  standalone: true,
  imports: [
    CommonModule,
    CurrencyPipe,
    DatePipe,
    MaterialGlobalModule,
    MaterialFormsModule,
    MaterialDatepickerModule,
  ],
  templateUrl: './lancamentos.component.html',
  styleUrl:    './lancamentos.component.scss',
})
export class LancamentosComponent implements OnInit {
  private fb       = inject(FormBuilder);
  private router   = inject(Router);
  private dialog   = inject(MatDialog);
  private lancSvc  = inject(LancamentoService);
  private finalSvc = inject(FinalidadeService);
  private toast    = inject(ToastService);

  formFilters!: FormGroup;
  result: PageTemplate<Lancamento> = new PageTemplate<Lancamento>();
  loading    = false;
  pageIndex  = 0;
  pageSize   = 10;

  finalidades:  Finalidade[] = [];
  tipoOpcoes   = TipoLancamento.opcoesTipoTodos;
  statusOpcoes = StatusLancamento.opcoesStatusLancamentoTodos;

  readonly TipoLancamento   = TipoLancamento;
  readonly StatusLancamento = StatusLancamento;
  readonly FormaPagamento   = FormaPagamento;

  displayedColumns = ['data_pagamento', 'descricao', 'finalidade', 'forma_pagamento', 'valor', 'status', 'acoes'];

  ngOnInit(): void {
    this.formFilters = this.fb.group({
      data_inicio:   [moment().startOf('month')],
      data_fim:      [moment()],
      tipo:          [TipoLancamento.TODOS],
      status:        [StatusLancamento.TODOS],
      finalidade_id: [-1],
    });

    this.finalSvc.listAll().subscribe({
      next: (data) => { this.finalidades = data; this.buscar(); },
      error: ()    => this.buscar(),
    });
  }

  buscar(): void {
    this.pageIndex = 0;
    this.load();
  }

  load(): void {
    this.loading = true;
    this.lancSvc.list(this.buildFilter(), { skip: this.pageIndex * this.pageSize, limit: this.pageSize }).subscribe({
      next: (data) => { this.result = data; this.loading = false; },
      error: ()    => { this.loading = false; },
    });
  }

  onPage(event: PageEvent): void {
    this.pageIndex = event.pageIndex;
    this.pageSize  = event.pageSize;
    this.load();
  }

  criar(): void  { this.router.navigate(['/lancamentos/novo']); }
  editar(id: number): void { this.router.navigate(['/lancamentos', id, 'editar']); }

  deletar(l: Lancamento): void {
    const valor = l.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    this.dialog.open(ConfirmDialogComponent, {
      width: '420px',
      data: {
        title:   'Confirmar exclusão',
        message: `Deseja deletar o lançamento de ${TipoLancamento.getTipoDescricao(l.tipo)} "${l.descricao}" no valor de R$ ${valor}?`,
      },
    }).afterClosed().subscribe((ok: boolean) => {
      if (!ok) return;
      this.lancSvc.remover(l.id).subscribe({
        next: () => {
          this.toast.success({ message: 'Lançamento excluído com sucesso.' });
          this.load();
        },
        error: (err) => this.toast.error({ message: err?.error?.detail ?? 'Erro ao excluir lançamento.' }),
      });
    });
  }

  getFinalidade(l: Lancamento): string {
    return l.sugestao_finalidade?.nome ?? '—';
  }

  private buildFilter() {
    const { data_inicio, data_fim, tipo, status, finalidade_id } = this.formFilters.value;
    return {
      ...(data_inicio   && { data_inicio: moment(data_inicio).format('YYYY-MM-DDT00:00:00') }),
      ...(data_fim      && { data_fim:    moment(data_fim).format('YYYY-MM-DDT23:59:59') }),
      ...(tipo          && { tipo }),
      ...(status        && { status }),
      ...(finalidade_id !== -1 && { finalidade_id: Number(finalidade_id) }),
    };
  }
}
