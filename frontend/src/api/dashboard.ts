import axios from 'axios';
import { PersonRes } from './person';
import { OrgRes } from './org';

export interface DashboardRes {
    docNumber: number;
    personNumber: number;
    orgNumber: number;
}

export interface HotRes {
    hotOrgs: OrgRes[];
    hotPersons: PersonRes[];
}


export function queyDashboard(): Promise<DashboardRes> {
    return axios.get(`/api/v1/data/dashboard/index`);
}

export function queryDashboardHot(): Promise<HotRes> {
    return axios.get(`/api/v1/data/dashboard/hot`)
}
  