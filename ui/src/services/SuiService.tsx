import _axios from '../config/axios';
import { ExampleTestReponse } from '../types/sui/response';

/**
 * Makes a test call to the server.
 * @returns A promise that resolves to an ExampleTestReponse object.
 */
export async function testCall(): Promise<ExampleTestReponse> {
    const response = await _axios.get('/test');
    return response.data;
}
