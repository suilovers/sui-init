// ----------------------------------------------------------------------

import { LazyExoticComponent, Suspense, lazy } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

/**
 * A higher-order component that wraps a lazy-loaded component with a `Suspense` component
 * and a loading screen fallback.
 * @param Component - The lazy-loaded component to wrap.
 * @returns A new component that renders the lazy-loaded component with a `Suspense` component
 * and a loading screen fallback.
 */
function Loadable(Component: LazyExoticComponent<() => JSX.Element>) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return function (props: any) {
        return (
            <Suspense
            // fallback={<LoadingScreen />}
            >
                <Component {...props} />
            </Suspense>
        );
    };
}

export default function Router() {
    return (
        <RouterProvider
            router={createBrowserRouter([
                {
                    path: '',
                    children: [
                        {
                            path: '/',
                            element: <DashboardPage />
                        }
                    ]
                }
            ])}
        />
    );
}

const DashboardPage = Loadable(lazy(() => import('../pages/DashboardPage')));
