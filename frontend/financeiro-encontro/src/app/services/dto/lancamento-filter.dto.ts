export interface LancamentoFilterDto {
  data_inicio?:   string;
  data_fim?:      string;
  status?:        string;
  tipo?:          string;
  finalidade_id?: number;
  descricao?:     string;
  exclude_ids?:   number[];  // IDs já carregados (lazy load optimization)
}
