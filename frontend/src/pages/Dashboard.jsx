import { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';

function Dashboard() {
    const [metrics, setMetrics] = useState(null);
    const [filters, setFilters] = useState({
        unit_id: '',
        category_id: '',
        start_date: '',
        end_date: '',
    });
    const [loading, setLoading] = useState(true);
    const [showMovementDetails, setShowMovementDetails] = useState(false);

    useEffect(() => {
        fetchMetrics();
    }, []);

    const fetchMetrics = async () => {
        setLoading(true);
        try {
            const params = {};
            if (filters.unit_id) params.unit_id = filters.unit_id;
            if (filters.category_id) params.category_id = filters.category_id;
            if (filters.start_date) params.start_date = filters.start_date;
            if (filters.end_date) params.end_date = filters.end_date;

            const response = await dashboardAPI.getMetrics(params);
            setMetrics(response.data);
        } catch (error) {
            console.error('Failed to fetch metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleFilterChange = (e) => {
        setFilters({ ...filters, [e.target.name]: e.target.value });
    };

    const applyFilters = () => {
        fetchMetrics();
    };

    if (loading && !metrics) {
        return <div className="flex items-center justify-center h-screen">Loading...</div>;
    }

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

            {/* Filters */}
            <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-lg font-semibold mb-4">Filters</h2>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                        <input
                            type="date"
                            name="start_date"
                            value={filters.start_date}
                            onChange={handleFilterChange}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                        <input
                            type="date"
                            name="end_date"
                            value={filters.end_date}
                            onChange={handleFilterChange}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Unit ID</label>
                        <input
                            type="number"
                            name="unit_id"
                            value={filters.unit_id}
                            onChange={handleFilterChange}
                            placeholder="Enter unit ID"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Category ID</label>
                        <input
                            type="number"
                            name="category_id"
                            value={filters.category_id}
                            onChange={handleFilterChange}
                            placeholder="Enter category ID"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                </div>
                <button
                    onClick={applyFilters}
                    className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                >
                    Apply Filters
                </button>
            </div>

            {/* Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                <MetricCard
                    title="Opening Balance"
                    value={metrics?.opening_balance || 0}
                    color="blue"
                />
                <MetricCard
                    title="Closing Balance"
                    value={metrics?.closing_balance || 0}
                    color="green"
                />
                <MetricCard
                    title="Net Movement"
                    value={metrics?.net_movement || 0}
                    color="purple"
                    onClick={() => setShowMovementDetails(true)}
                    clickable
                />
                <MetricCard
                    title="Total Value"
                    value={`$${metrics?.total_value || 0}`}
                    color="yellow"
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                    title="Purchases"
                    value={metrics?.purchases || 0}
                    color="indigo"
                />
                <MetricCard
                    title="Transfer In"
                    value={metrics?.transfer_in || 0}
                    color="teal"
                />
                <MetricCard
                    title="Transfer Out"
                    value={metrics?.transfer_out || 0}
                    color="red"
                />
                <MetricCard
                    title="Assigned"
                    value={metrics?.assigned || 0}
                    color="orange"
                />
            </div>

            {/* Movement Details Modal */}
            {showMovementDetails && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-lg p-6 max-w-md w-full">
                        <h3 className="text-xl font-bold mb-4">Net Movement Details</h3>
                        <div className="space-y-3">
                            <div className="flex justify-between">
                                <span>Purchases:</span>
                                <span className="font-semibold">+{metrics?.purchases || 0}</span>
                            </div>
                            <div className="flex justify-between">
                                <span>Transfer In:</span>
                                <span className="font-semibold">+{metrics?.transfer_in || 0}</span>
                            </div>
                            <div className="flex justify-between">
                                <span>Transfer Out:</span>
                                <span className="font-semibold text-red-600">-{metrics?.transfer_out || 0}</span>
                            </div>
                            <div className="border-t pt-3 flex justify-between font-bold">
                                <span>Net Movement:</span>
                                <span>{metrics?.net_movement || 0}</span>
                            </div>
                        </div>
                        <button
                            onClick={() => setShowMovementDetails(false)}
                            className="mt-6 w-full bg-gray-600 hover:bg-gray-700 text-white py-2 rounded-lg"
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

function MetricCard({ title, value, color, onClick, clickable }) {
    const colors = {
        blue: 'from-blue-500 to-blue-600',
        green: 'from-green-500 to-green-600',
        purple: 'from-purple-500 to-purple-600',
        yellow: 'from-yellow-500 to-yellow-600',
        indigo: 'from-indigo-500 to-indigo-600',
        teal: 'from-teal-500 to-teal-600',
        red: 'from-red-500 to-red-600',
        orange: 'from-orange-500 to-orange-600',
    };

    return (
        <div
            className={`bg-gradient-to-br ${colors[color]} rounded-lg shadow-lg p-6 text-white ${clickable ? 'cursor-pointer hover:shadow-xl transform hover:scale-105 transition' : ''
                }`}
            onClick={onClick}
        >
            <h3 className="text-sm font-medium opacity-90 mb-2">{title}</h3>
            <p className="text-3xl font-bold">{value}</p>
            {clickable && <p className="text-xs mt-2 opacity-75">Click for details</p>}
        </div>
    );
}

export default Dashboard;
