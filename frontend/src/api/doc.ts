import axios from 'axios';
import qs from 'query-string';

export interface DocReq {
  title: string;
  content?: string;
  subject?: string;
  location?: string;
  source?: string;
  time?: string;
  persons?: [];
  orgs?: [];
  tags?: string [];
  follow?: boolean;
}

export interface DocRes extends DocReq {
  id: number;
}

export interface DocParams {
  title?: string;
  follow?: boolean;
  tags?: number[];
  page?: number;
  size?: number;
}

export interface DocListRes {
  items: DocRes[];
  total: number;
}

export interface DocDeleteParams {
  pk: number[];
}

export function queryDocList(params: DocParams): Promise<DocListRes> {
  return axios.get('/api/v1/data/docs', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function queryDocAll(params: DocParams): Promise<DocRes[]> {
  return axios.get('/api/v1/data/docs/all', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function queryDocDetail(pk: number): Promise<DocRes> {
  return axios.get(`/api/v1/data/docs/${pk}`);
}

export function createDocApi(data: DocReq) {
  return axios.post('/api/v1/data/docs', data);
}

export function updateDocApi(pk: number, data: DocReq) {
  return axios.put(`/api/v1/data/docs/${pk}`, data);
}

export function followDocApi(pk: number) {
  const params = {
    id: pk
  }
  return axios.get(`/api/v1/data/docs/follow`, {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function unfollowDocApi(pk: number) {
  const params = {
    id: pk
  }
  return axios.get(`/api/v1/data/docs/unfollow`, {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function downloadDocApi(uid: string) {
  return axios.get(`/api/v1/data/docs/download/${uid}`);
}

export function previewDocApi(uid: string) {
  return axios.get(`/api/v1/data/docs/preview/${uid}`);
}

export function uploadDocApi(data: FormData) {
  return axios.post(`/api/v1/data/docs/upload`, data);
}

export function deleteDocApi(params: DocDeleteParams) {
  return axios.delete(`/api/v1/data/docs`, {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}
