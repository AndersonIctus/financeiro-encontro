import { PerfilUsuario } from '../usuario.model';

export class Perfil {
  static readonly ADMINISTRADOR: PerfilUsuario = 'ADMINISTRADOR';
  static readonly CONCILIADOR:   PerfilUsuario = 'CONCILIADOR';
  static readonly REPORTER:      PerfilUsuario = 'REPORTER';

  static readonly opcoes = [
    { value: 'ADMINISTRADOR', label: 'Administrador' },
    { value: 'CONCILIADOR',   label: 'Conciliador'   },
    { value: 'REPORTER',      label: 'Reporter'      },
  ];
}
