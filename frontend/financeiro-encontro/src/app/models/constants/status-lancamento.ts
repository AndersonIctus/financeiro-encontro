export class StatusLancamento {
  static CONCILIADO     = 'CONCILIADO';
  static NAO_CONCILIADO = 'NAO_CONCILIADO';
  static TODOS          = '';

  static get opcoesStatusLancamentoTodos() {
    return [
      { name: 'Todos',          value: StatusLancamento.TODOS          },
      { name: 'Conciliado',     value: StatusLancamento.CONCILIADO     },
      { name: 'Não Conciliado', value: StatusLancamento.NAO_CONCILIADO },
    ];
  }

  static get opcoesStatusLancamento() {
    return [
      { name: 'Conciliado',     value: StatusLancamento.CONCILIADO     },
      { name: 'Não Conciliado', value: StatusLancamento.NAO_CONCILIADO },
    ];
  }

  static getStatusLancamentoDescricao(status: string): string {
    switch (status) {
      default:                                  return 'Desconhecido';
      case StatusLancamento.CONCILIADO:         return 'Conciliado';
      case StatusLancamento.NAO_CONCILIADO:     return 'Não Conciliado';
    }
  }
}
