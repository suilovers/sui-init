import { JsonViewer, defineDataType } from '@textea/json-viewer';
import { DataGrid} from '@mui/x-data-grid';


interface CommandExecutionResultProps {
    response: any;
}
// uniqueidcreator
class UniqueIDGenerator {
    private static instance: UniqueIDGenerator;
    private idCounter: number;

    private constructor() {
        this.idCounter = 0;
    }

    public static getInstance(): UniqueIDGenerator {
        if (!UniqueIDGenerator.instance) {
            UniqueIDGenerator.instance = new UniqueIDGenerator();
        }
        return UniqueIDGenerator.instance;
    }

    public generateID(): string {
        // Generate a unique ID using a combination of timestamp and idCounter
        const timestamp = new Date().getTime().toString(36);
        this.idCounter++;
        return `${timestamp}-${this.idCounter.toString(36)}`;
    }
}

export default function CommandExecutionResult({ response }: CommandExecutionResultProps) {
    const idGenerator = UniqueIDGenerator.getInstance();
    const addressDataType = defineDataType({
        is: (value:any) => typeof value === 'string' && value.startsWith('0x'),
        Component: (props:any) => <span style={{ color: 'green' }}>{props.value}</span>
      })
    const stringArrayDataType = defineDataType({
        is: (value:any) => Array.isArray(value) && value.every((item:any) => typeof item === 'string'),
        Component: (props:any) =>
        <DataGrid 
            columns={[{ field: "field1",headerName:props.path, width: 1000, editable:false}]} 
            rows={props.value.map((item:any) => ({id: idGenerator.generateID(), field1: item}))}
            getRowId={(item: any) => item.id}

        />
      })
    const objectArrayDataType = defineDataType({
        is: (value:any) => Array.isArray(value) && value.every((item:any) => typeof item === 'object'),
        Component: (props:any) =>
<DataGrid 
    columns={Object.keys(props.value[0]).map((key:any) => ({ 
        field: key,
        headerName: key, 
        width: props.value.reduce((max:number, item:any) => {
            let valueLength = item[key] ? item[key].toString().length : 0;
            return Math.max(max, valueLength * 10);
        }, 200), 
        editable: false
    }))} 
    rows={props.value.map((item:any) => {
        let row:any = { id: idGenerator.generateID() };
        Object.keys(item).forEach(key => {
            row[key] = item[key] !== null ? item[key] : ""; // null değerleri boş dizeyle değiştir
        });
        return row;
    })}
    getRowId={(item: any) => item.id}
/>
      })

    return <JsonViewer rootName={false} theme="dark" value={response} valueTypes={[addressDataType,stringArrayDataType,objectArrayDataType]}/>;
}
