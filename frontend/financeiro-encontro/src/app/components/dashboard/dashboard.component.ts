import { Component, OnInit } from '@angular/core';
import { CommonModule, CurrencyPipe, DecimalPipe } from '@angular/common';
import { FormBuilder, FormGroup } from '@angular/forms';
import moment from 'moment';

import {
  MaterialGlobalModule,
  MaterialFormsModule,
  MaterialDatepickerModule,
} from '../../shared/modules/material.imports.module';
import { DashboardService } from '../../services/dashboard.service';
import { DashboardTotais } from '../../models/dashboard.model';
import { DashboardFilterDto } from '../../services/dto/dashboard-filter.dto';
import { TipoLancamento } from '../../models/constants/tipo-lancamento';
import { StatusLancamento } from '../../models/constants/status-lancamento';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    CurrencyPipe,
    DecimalPipe,
    MaterialGlobalModule,
    MaterialFormsModule,
    MaterialDatepickerModule,
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements OnInit {
  form: FormGroup;
  totais: DashboardTotais | null = null;
  loading = false;

  tipoOpcoes = TipoLancamento.opcoesTipoTodos;
  statusOpcoes = StatusLancamento.opcoesStatusLancamentoTodos;

  constructor(
    private fb: FormBuilder,
    private dashboardService: DashboardService,
  ) {
    this.form = this.fb.group({
      data_inicio: [moment().startOf('month')],
      data_fim:    [moment()],
      tipo:        [TipoLancamento.TODOS],
      status:      [StatusLancamento.TODOS],
    });
  }

  ngOnInit(): void {
    this.buscar();
  }

  buscar(): void {
    const filter = this.buildFilter();
    this.loading = true;
    this.dashboardService.getTotais(filter).subscribe({
      next: data  => { this.totais = data;  this.loading = false; },
      error: ()   => {                      this.loading = false; },
    });
  }

  private buildFilter(): DashboardFilterDto {
    const { data_inicio, data_fim, tipo, status } = this.form.value;
    return {
      data_inicio: data_inicio ? moment(data_inicio).format('YYYY-MM-DD') : undefined,
      data_fim:    data_fim    ? moment(data_fim).format('YYYY-MM-DD')    : undefined,
      tipo:        tipo   || undefined,
      status:      status || undefined,
    };
  }
}
