import { CommandDTO } from '../types/sui/response';

/**
 * Converts a command map object into a list of CommandDTO objects.
 *
 * @param commandMap - The command map object to convert.
 * @returns An array of CommandDTO objects.
 */
export function convertCommandMapToList(commandMap: Object): CommandDTO[] {
    const commandList = [] as CommandDTO[];
    Object.entries(commandMap).forEach(([key, value]): void => {
        const command = value['/'] as CommandDTO;
        command.childs = [];
        // eslint-disable-next-line @typescript-eslint/no-use-before-define
        for (const [innerKey, innerValue] of Object.entries(value as Object)) {
            if (innerKey !== '/') {
                command.childs.push(innerValue as CommandDTO);
            }
        }

        commandList.push(command);
    });
    return commandList;
}
