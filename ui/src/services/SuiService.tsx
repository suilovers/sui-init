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

/**
 * Retrieves the list of commands from the server.
 * @returns A promise that resolves to an array of CommandDTO objects.
 */
export async function fetchCommandList() {
    const response = await _axios.post('/command/all');
    return response.data;
}

/**
 * Fetches command data from the server.
 *
 * @param parentCommand - The parent command.
 * @param childCommand - The child command.
 * @returns A Promise that resolves to the fetched command data.
 */
export async function fetchCommand(parentCommand: string, childCommand: string) {
    const response = await _axios.post(`/command`, {
        paths: [`/${parentCommand}`, `/${childCommand}`]
    });
    return response.data;
}

/**
 * Fetches data from the specified path using Axios.
 * @param path - The path to fetch data from.
 * @returns A Promise that resolves to the fetched data.
 */
export async function fetchCall(path: string) {
    const response = await _axios.post(path);

    if (response) {
        return response.data;
    }
    return false;
}

export async function fetchCallWithArguments(path: string, argumentBodyNames: any, optionsBodyNames: any, argumentValues: any, optionValues: any) {
    const body: any = {};

    argumentBodyNames.forEach((key: any, index: any) => {
        body[key] = argumentValues[index];
    });

    if (optionsBodyNames && optionValues) {
        optionsBodyNames.forEach((key: any, index: any) => {
            body[key] = optionValues[index];
        });
    }

    const response = await _axios.post(path, body).catch((error) => {
        console.log(error);
    });
    if (response) {
        return response.data;
    }
    return false;
}
