import axios from 'axios';


export interface OCRRes {
    ocr_res: string[];
    content: string;
}

export function ocrDoc(pk: number): Promise<OCRRes> {
    return axios.get(`/api/v1/data/ocr/ocr_doc/${pk}`);
}
  