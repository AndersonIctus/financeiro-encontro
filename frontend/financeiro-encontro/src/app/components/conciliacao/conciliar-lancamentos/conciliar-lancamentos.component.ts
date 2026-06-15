import {
  Component,
  OnInit,
  OnDestroy,
  ChangeDetectorRef,
  inject,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import {
  animate,
  AnimationEvent,
  keyframes,
  state,
  style,
  transition,
  trigger,
} from '@angular/animations';
import { Subject, Subscription } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

import { MaterialGlobalModule, MaterialFormsModule } from '../../../shared/modules/material.imports.module';
import { ConciliacaoCardComponent } from './conciliacao-card/conciliacao-card.component';
import { LancamentoService } from '../../../services/lancamento.service';
import { FinalidadeService } from '../../../services/finalidade.service';
import { Lancamento } from '../../../models/lancamento.model';
import { Finalidade } from '../../../models/finalidade.model';
import { StatusLancamento } from '../../../models/constants/status-lancamento';

interface CardItem extends Lancamento {
  _state: 'visible' | 'leaving';
}

@Component({
  selector: 'app-conciliar-lancamentos',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MaterialGlobalModule,
    MaterialFormsModule,
    ConciliacaoCardComponent,
  ],
  templateUrl: './conciliar-lancamentos.component.html',
  styleUrl: './conciliar-lancamentos.component.scss',
  animations: [
    trigger('cardLeave', [
      state('visible', style({ opacity: 1 })),
      state('leaving', style({ opacity: 0 })),
      transition('visible => leaving', [
        style({ overflow: 'hidden' }),
        animate(
          '350ms ease-in-out',
          keyframes([
            style({ opacity: 1, height: '*', marginBottom: '*', paddingTop: '*', paddingBottom: '*', offset: 0 }),
            style({ opacity: 0, height: '*', marginBottom: '*', paddingTop: '*', paddingBottom: '*', offset: 0.4 }),
            style({ opacity: 0, height: '0px', marginBottom: '0px', paddingTop: '0px', paddingBottom: '0px', offset: 1 }),
          ]),
        ),
      ]),
    ]),
  ],
})
export class ConciliarLancamentosComponent implements OnInit, OnDestroy {
  private lancamentoService = inject(LancamentoService);
  private finalidadeService = inject(FinalidadeService);
  private router            = inject(Router);
  private cdr               = inject(ChangeDetectorRef);

  items: CardItem[]     = [];
  finalidades: Finalidade[] = [];
  loading     = false;
  loadingMore = false;
  allLoaded   = false;
  search      = '';

  private searchSubject = new Subject<string>();
  private searchSub!: Subscription;

  ngOnInit(): void {
    this.searchSub = this.searchSubject.pipe(
      debounceTime(300),
      distinctUntilChanged(),
    ).subscribe(() => this.reset());

    this.finalidadeService.listAll().subscribe({
      next: (data) => {
        this.finalidades = data;
        this.loadBatch(true);
      },
      error: () => this.loadBatch(true),
    });
  }

  ngOnDestroy(): void {
    this.searchSub?.unsubscribe();
  }

  onSearchChange(): void {
    this.searchSubject.next(this.search);
  }

  voltar(): void {
    this.router.navigate(['/conciliacao']);
  }

  private reset(): void {
    this.items     = [];
    this.allLoaded = false;
    this.loadBatch(true);
  }

  loadBatch(initial = false): void {
    if (initial) {
      this.loading = true;
    } else {
      this.loadingMore = true;
    }

    const skip = this.visibleItems.length;

    this.lancamentoService
      .list(
        {
          status:    StatusLancamento.NAO_CONCILIADO,
          ...(this.search ? { descricao: this.search } : {}),
        },
        { skip, limit: 20 },
      )
      .subscribe({
        next: (page) => {
          const newItems: CardItem[] = page.items.map(l => ({ ...l, _state: 'visible' }));
          this.items = [...this.visibleItems, ...newItems];
          if (page.items.length < 20) this.allLoaded = true;
          this.loading     = false;
          this.loadingMore = false;
          this.cdr.detectChanges();
        },
        error: () => {
          this.loading     = false;
          this.loadingMore = false;
          this.cdr.detectChanges();
        },
      });
  }

  onConciliado(item: CardItem): void {
    item._state = 'leaving';
  }

  onLeaveDone(event: AnimationEvent, item: CardItem): void {
    if (event.toState !== 'leaving') return;
    this.items = this.items.filter(i => i.id !== item.id);
    this.cdr.detectChanges();

    if (this.visibleItems.length < 15 && !this.allLoaded && !this.loadingMore) {
      this.loadBatch();
    }
  }

  get visibleItems(): CardItem[] {
    return this.items.filter(i => i._state === 'visible');
  }

  get isEmpty(): boolean {
    return !this.loading && this.items.length === 0;
  }
}
