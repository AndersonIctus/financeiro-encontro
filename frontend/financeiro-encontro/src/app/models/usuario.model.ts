export type PerfilUsuario = 'ADMINISTRADOR' | 'CONCILIADOR' | 'REPORTER';

export interface Usuario {
  id: number;
  nome: string;
  email: string;
  ativo: boolean;
  perfil: PerfilUsuario;
  criado_em: string;
}
