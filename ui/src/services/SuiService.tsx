import { EnvironmentData, NetworkType } from '../config';
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
 * Switches the network to the specified network type.
 * @param network The network type to switch to.
 * @returns A Promise that resolves to the response data from the server.
 */
export async function switchNetwork(network: NetworkType) {
    const response = await _axios.post('/client/switch', {
        env: network
    });
    return response.data;
}

/**
 * Fetches the local network data.
 * @returns A Promise that resolves to a boolean indicating the success of the request.
 */
export async function checkLocalNetwork(): Promise<boolean> {
    const response = await _axios.post('/network/check-local-network');
    return response.data;
}

/**
 * Retrieves the network environments.
 * @returns A Promise that resolves to an object containing the network environments.
 */
export async function getNetworkEnvironments(): Promise<{ [key in NetworkType]: EnvironmentData }> {
    const response = await _axios.post('/network/environments');
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

export async function fetchCallWithBody(path: string, body: any) {
    const response = await _axios.post(path, body);

    if (response) {
        return response.data;
    }
    return false;
}

/**
 * Makes a POST request to the specified path with the provided arguments and options.
 * @param {string} path - The path to make the request to.
 * @param {any[]} argumentBodyNames - An array of argument body names.
 * @param {any[]} optionsBodyNames - An array of options body names.
 * @param {any[]} argumentValues - An array of argument values.
 * @param {any[]} optionValues - An array of option values.
 * @returns {Promise<any>} - A promise that resolves to the response data if successful, or false if there was an error.
 */
export async function fetchCallWithArguments(
    path: string,
    argumentBodyNames: any[],
    optionsBodyNames: any[],
    argumentValues: any[],
    optionValues: any[]
): Promise<any> {
    const body: any = {};

    argumentBodyNames.forEach((key: any, index: any) => {
        body[key] = argumentValues[index];
    });

    if (optionsBodyNames && optionValues) {
        optionsBodyNames.forEach((key: any, index: any) => {
            body[key] = optionValues[index];
        });
    }

    const response = await _axios.post(path, body);
    return response.data;
}
