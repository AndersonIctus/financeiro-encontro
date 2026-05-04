export interface DashboardTotais {
  total_receitas: number;
  total_despesas: number;
  saldo:          number;
  quantidade:     number;
}

export interface DashboardPorDia {
  dia:            string;
  total_receitas: number;
  total_despesas: number;
  saldo:          number;
}

export interface DashboardPorMes {
  mes:            string;
  total_receitas: number;
  total_despesas: number;
  saldo:          number;
}
