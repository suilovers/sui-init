import { useState } from 'react';

export function useToggle(initialState: boolean): [boolean, () => void] {
    const [state, setState] = useState<boolean>(initialState);

    const toggle = () => {
        setState((prevState) => !prevState);
    };

    return [state, toggle];
}
