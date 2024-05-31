import { useState } from 'react';

export default function SuiScanDashboardPage() {
    const [url, setUrl] = useState<string>('');
    return (
        <div
            style={{
                width: '100vw',
                height: '100vh'
            }}
        >
            <iframe width="100%" height="100%" src="https://custom.suiscan.xyz/custom/home/?network=http%3A%2F%2Flocalhost%3A8000" />
        </div>
    );
}
