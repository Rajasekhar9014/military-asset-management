import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';

function Layout() {
    const navigate = useNavigate();
    const location = useLocation();
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
    };

    const isActive = (path) => {
        return location.pathname === path;
    };

    return (
        <div className="min-h-screen bg-gray-100">
            {/* Navigation */}
            <nav className="bg-gradient-to-r from-blue-900 to-blue-700 shadow-lg">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <div className="flex-shrink-0 flex items-center">
                                <h1 className="text-white text-xl font-bold">Military Asset Management</h1>
                            </div>
                            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                <Link
                                    to="/dashboard"
                                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${isActive('/dashboard')
                                            ? 'border-white text-white'
                                            : 'border-transparent text-blue-100 hover:border-blue-300 hover:text-white'
                                        }`}
                                >
                                    Dashboard
                                </Link>
                                <Link
                                    to="/purchases"
                                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${isActive('/purchases')
                                            ? 'border-white text-white'
                                            : 'border-transparent text-blue-100 hover:border-blue-300 hover:text-white'
                                        }`}
                                >
                                    Purchases
                                </Link>
                                <Link
                                    to="/transfers"
                                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${isActive('/transfers')
                                            ? 'border-white text-white'
                                            : 'border-transparent text-blue-100 hover:border-blue-300 hover:text-white'
                                        }`}
                                >
                                    Transfers
                                </Link>
                            </div>
                        </div>
                        <div className="flex items-center">
                            <span className="text-white mr-4">
                                Welcome, <span className="font-semibold">{user.username || 'User'}</span>
                            </span>
                            <button
                                onClick={handleLogout}
                                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <Outlet />
            </main>
        </div>
    );
}

export default Layout;
