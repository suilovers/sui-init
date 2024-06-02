import { Button } from '@mui/material';
import CustomForm from '../../component/CustomForm'; // Ensure CustomForm is imported correctly

const MoveMenuButton = ({
    buttonText,
    buttonLabel,
    placeholder,
    run,
    changeChildren,
    formRun,
    changeInput
}: {
    buttonText: string;
    buttonLabel: string;
    placeholder: string;
    run: () => void;
    changeChildren: (children: any) => void;
    formRun: () => void;
    changeInput: (e: any) => void;
}) => {
    return (
        <Button
            style={{
                width: '100%',
                marginBottom: '10px'
            }}
            variant="contained"
            onClick={() => {
                run();
                changeChildren(<CustomForm changeInput={changeInput} buttonLabel={buttonLabel} placeholder={placeholder} run={formRun} />);
            }}
        >
            {buttonText}
        </Button>
    );
};

export default MoveMenuButton;
