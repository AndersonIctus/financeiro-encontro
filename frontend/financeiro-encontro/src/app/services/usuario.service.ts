import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AbstractService } from './abstract.service';
import { Usuario } from '../models/usuario.model';
import { PageTemplate, PageRequest } from './util/PageTemplate';

export interface UsuarioCreate {
  nome:   string;
  email:  string;
  senha:  string;
  ativo:  boolean;
}

export interface UsuarioUpdate {
  nome:   string;
  email:  string;
  senha?: string;
  ativo:  boolean;
}

@Injectable({ providedIn: 'root' })
export class UsuarioService extends AbstractService<Usuario> {
  constructor(http: HttpClient) {
    super(http, 'usuarios');
  }

  list(pagination?: PageRequest): Observable<PageTemplate<Usuario>> {
    const params = { ...pagination };
    return this.getCustom<PageTemplate<Usuario>>('', { params });
  }

  buscarPorId(id: number): Observable<Usuario> {
    return this.getById(id);
  }

  criar(data: UsuarioCreate): Observable<Usuario> {
    return this.persist<Usuario>(data);
  }

  editar(id: number, data: UsuarioUpdate): Observable<Usuario> {
    return this.update<Usuario>(data, id);
  }

  remover(id: number): Observable<null> {
    return this.delete(id);
  }
}
