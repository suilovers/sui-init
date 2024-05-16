import { LazyExoticComponent, Suspense, lazy } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { CustomLayoutView } from '../layout';

/**
 * A higher-order component that wraps a lazy-loaded component with a `Suspense` component
 * and a loading screen fallback.
 * @param Component - The lazy-loaded component to wrap.
 * @returns A new component that renders the lazy-loaded component with a `Suspense` component
 * and a loading screen fallback.
 */
function Loadable(Component: LazyExoticComponent<() => JSX.Element>) {
    return function (props: any) {
        return (
            <Suspense>
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
                    element: <CustomLayoutView />,
                    children: [
                        {
                            path: '/',
                            element: <DashboardPage />
                        },
                        {
                            path: 'editor',
                            element: <MoveEditorPage />
                        },
                        {
                            path: ':parentCommand/:childCommand',
                            element: <CommandExecutionPage />
                        }
                    ]
                }
            ])}
        />
    );
}

const DashboardPage = Loadable(lazy(() => import('../pages/DashboardPage')));
const CommandExecutionPage = Loadable(lazy(() => import('../pages/CommandExecutionPage')));
const MoveEditorPage = Loadable(lazy(() => import('../pages/MoveEditorPage')));
