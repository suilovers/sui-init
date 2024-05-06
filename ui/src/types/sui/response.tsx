export type ExampleTestReponse = {};

export interface Argument {
    default: string;
    description: string;
    name: string;
    title: string;
    type: string;
}

export interface OptionalArgument {
    default: string;
    description: string;
    name: string;
    title: string;
    type: string;
}

export interface CommandDTO {
    arguments: Argument[];
    description: string;
    name: string;
    optionalArguments: OptionalArgument[];
    path: string;
}