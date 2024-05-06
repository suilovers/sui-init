import _axios from '../config/axios';
import { CommandDTO, ExampleTestReponse } from '../types/sui/response';

/**
 * Makes a test call to the server.
 * @returns A promise that resolves to an ExampleTestReponse object.
 */
export async function testCall(): Promise<ExampleTestReponse> {
    const response = await _axios.get('/test');
    return response.data;
}

/**
 * Retrieves the list of commands from the server.
 * @returns A promise that resolves to an array of CommandDTO objects.
 */
export async function getCommandList(): Promise<CommandDTO[]> {
    const response = await _axios.get('/info');
    return response.data;
}
