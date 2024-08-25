import axios from 'axios';
import qs from 'query-string';

export interface SubjectReq {
  name: string;
  type: string;
  detail: string;
  docs: [];
  persons: [];
  orgs: [];
  his: SubjectHisParams [];
}

export interface SubjectRes extends SubjectReq {
  id: number;
}

export interface SubjectParams {
  name?: string;
  page?: number;
  size?: number;
}

export interface SubjectListRes {
  items: SubjectRes[];
  total: number;
}

export interface SubjectDeleteParams {
  pk: number[];
}

export interface SubjectHisParams {
  index: number;
  title: string | undefined;
  detail: string | undefined;
}

export function querySubjectList(params: SubjectParams): Promise<SubjectListRes> {
  return axios.get('/api/v1/data/subjects', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function querySubjectAll(): Promise<SubjectRes[]> {
  return axios.get('/api/v1/data/subjects/all');
}

export function querySubjectDetail(pk: number): Promise<SubjectRes> {
  return axios.get(`/api/v1/data/subjects/${pk}`);
}

export function createSubjectApi(data: SubjectReq) {
  return axios.post('/api/v1/data/subjects', data);
}

export function updateSubjectApi(pk: number, data: SubjectReq) {
  return axios.put(`/api/v1/data/subjects/${pk}`, data);
}

export function deleteSubjectApi(params: SubjectDeleteParams) {
  return axios.delete(`/api/v1/data/subjects`, {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}
