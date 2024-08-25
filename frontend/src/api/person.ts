import axios from 'axios';
import qs from 'query-string';
import { DocRes } from './doc';
import { OrgRes } from './org';

export interface PersonReq {
  name: string;
  sex?: number;
  job?: string;
  org_name?: string;
  nation?: string;
  birth_date?: Date;
  birth_addr?: string;
  school?: string;
  country?: string;
  detail?: string;
  docs: DocRes[];
  orgs: OrgRes[];
  persons: PersonRes[];
  attachments: Record<string, any>[];
  relations: PersonRelationReq[];
}

export interface PersonRes extends PersonReq {
  id: number;
  icon?: string;
  relation_json: Record<string, any>;
}

export interface PersonParams {
  docs?: number[];
  name?: string;
  page?: number;
  size?: number;
}

export interface PersonListRes {
  items: PersonRes[];
  total: number;
}

export interface PersonDeleteParams {
  pk: number[];
}

export interface PersonRelationReq {
  index: number;
  other_id: number | undefined;
  detail: string | undefined;
}

export function queryPersonList(params: PersonParams): Promise<PersonListRes> {
  return axios.get('/api/v1/data/persons', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function queryPersonAll(params: PersonParams): Promise<PersonRes[]> {
  return axios.get('/api/v1/data/persons/all', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function queryPersonDetail(pk: number): Promise<PersonRes> {
  return axios.get(`/api/v1/data/persons/${pk}`);
}

export function createPersonApi(data: PersonReq) {
  return axios.post('/api/v1/data/persons', data);
}

export function updatePersonApi(pk: number, data: PersonReq) {
  return axios.put(`/api/v1/data/persons/${pk}`, data);
}

export function deletePersonApi(params: PersonDeleteParams) {
  return axios.delete(`/api/v1/data/persons`, {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}
