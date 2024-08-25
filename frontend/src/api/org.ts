import axios from 'axios';
import qs from 'query-string';

export interface OrgReq {
  name: string;
  parent_id?: number;
  location?: string;
  start_date?: Date;
  detail?: string;
  docs: [];
  persons: [];
}

export interface OrgRes extends OrgReq {
  id: number;
  parent: OrgRes;
}

export interface OrgParams {
  name?: string;
  page?: number;
  size?: number;
}

export interface OrgListRes {
  items: OrgRes[];
  total: number;
}

export interface OrgTreeRes extends OrgRes {
  children?: OrgRes[];
}

export interface OrgDeleteParams {
  pk: number[];
}

export function queryOrgList(params: OrgParams): Promise<OrgListRes> {
  return axios.get('/api/v1/data/orgs', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function queryOrgTree(params: OrgParams): Promise<OrgTreeRes[]> {
  return axios.get('/api/v1/data/orgs/tree', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function queryOrgAll(params: OrgParams): Promise<OrgRes[]> {
  return axios.get('/api/v1/data/orgs/all', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function queryOrgDetail(pk: number): Promise<OrgRes> {
  return axios.get(`/api/v1/data/orgs/${pk}`);
}

export function createOrgApi(data: OrgReq) {
  return axios.post('/api/v1/data/orgs', data);
}

export function updateOrgApi(pk: number, data: OrgReq) {
  return axios.put(`/api/v1/data/orgs/${pk}`, data);
}

export function deleteOrgApi(params: OrgDeleteParams) {
  return axios.delete(`/api/v1/data/orgs`, {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}
