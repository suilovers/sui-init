import React, { useState, useEffect, useRef } from 'react';

export default function SuiScanDashboardPage() {
    const [url, setUrl] = useState<string>('');
    const iframeRef = useRef<HTMLIFrameElement>(null);

    useEffect(() => {
        const iframe = iframeRef.current;
        if (iframe) {
            // Make sure the iframe content is loaded
            iframe.onload = () => {
                const iframeDocument = iframe.contentDocument || iframe.contentWindow?.document;
                if (iframeDocument) {
                    // Example: Change the background color of the body inside the iframe
                    iframeDocument.body.style.backgroundColor = 'lightblue';
                    
                    // Example: Add custom content inside the iframe
                    const customDiv = iframeDocument.createElement('div');
                    customDiv.innerHTML = '<p>This is custom content added to the iframe!</p>';
                    iframeDocument.body.appendChild(customDiv);
                }
            };
        }
    }, []);

    return (
        <div
            style={{
                width: '100vw',
                height: '100vh'
            }}
        >
            <iframe
                ref={iframeRef}
                width="100%"
                height="100%"
                src="https://custom.suiscan.xyz/custom/home/?network=http%3A%2F%2Flocalhost%3A8000"
            />
        </div>
    );
}