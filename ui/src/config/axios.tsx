import _axios from 'axios';
import { API_BASE_URL } from '../config';

let axios = _axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

export default axios;
