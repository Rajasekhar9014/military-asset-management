import { useState, useEffect } from 'react';
import { transfersAPI } from '../services/api';

function Transfers() {
    const [transfers, setTransfers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [filters, setFilters] = useState({
        unit_id: '',
        status_filter: '',
        start_date: '',
        end_date: '',
    });

    useEffect(() => {
        fetchTransfers();
    }, []);

    const fetchTransfers = async () => {
        setLoading(true);
        try {
            const params = {};
            if (filters.unit_id) params.unit_id = filters.unit_id;
            if (filters.status_filter) params.status_filter = filters.status_filter;
            if (filters.start_date) params.start_date = filters.start_date;
            if (filters.end_date) params.end_date = filters.end_date;

            const response = await transfersAPI.list(params);
            setTransfers(response.data);
        } catch (error) {
            console.error('Failed to fetch transfers:', error);
        } finally {
            setLoading(false);
        }
    };

    const getStatusColor = (status) => {
        const colors = {
            PENDING: 'bg-yellow-100 text-yellow-800',
            IN_TRANSIT: 'bg-blue-100 text-blue-800',
            COMPLETED: 'bg-green-100 text-green-800',
            CANCELLED: 'bg-red-100 text-red-800',
        };
        return colors[status] || 'bg-gray-100 text-gray-800';
    };

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Transfers</h1>
                <button
                    onClick={() => setShowForm(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                >
                    + New Transfer
                </button>
            </div>

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
                            onChange={(e) => setFilters({ ...filters, start_date: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                        <input
                            type="date"
                            name="end_date"
                            value={filters.end_date}
                            onChange={(e) => setFilters({ ...filters, end_date: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Unit ID</label>
                        <input
                            type="number"
                            name="unit_id"
                            value={filters.unit_id}
                            onChange={(e) => setFilters({ ...filters, unit_id: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                        <select
                            name="status_filter"
                            value={filters.status_filter}
                            onChange={(e) => setFilters({ ...filters, status_filter: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        >
                            <option value="">All</option>
                            <option value="PENDING">Pending</option>
                            <option value="IN_TRANSIT">In Transit</option>
                            <option value="COMPLETED">Completed</option>
                            <option value="CANCELLED">Cancelled</option>
                        </select>
                    </div>
                </div>
                <button
                    onClick={fetchTransfers}
                    className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                >
                    Apply Filters
                </button>
            </div>

            {/* Transfers Table */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Asset ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">From Unit</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">To Unit</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {loading ? (
                            <tr>
                                <td colSpan="7" className="px-6 py-4 text-center text-gray-500">
                                    Loading...
                                </td>
                            </tr>
                        ) : transfers.length === 0 ? (
                            <tr>
                                <td colSpan="7" className="px-6 py-4 text-center text-gray-500">
                                    No transfers found
                                </td>
                            </tr>
                        ) : (
                            transfers.map((transfer) => (
                                <tr key={transfer.id} className="hover:bg-gray-50">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{transfer.id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{transfer.asset_id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{transfer.from_unit_id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{transfer.to_unit_id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{transfer.quantity}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(transfer.status)}`}>
                                            {transfer.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                        {new Date(transfer.transfer_date).toLocaleDateString()}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* New Transfer Form Modal */}
            {showForm && (
                <TransferForm
                    onClose={() => setShowForm(false)}
                    onSuccess={() => {
                        setShowForm(false);
                        fetchTransfers();
                    }}
                />
            )}
        </div>
    );
}

function TransferForm({ onClose, onSuccess }) {
    const [formData, setFormData] = useState({
        asset_id: '',
        from_unit_id: '',
        to_unit_id: '',
        quantity: '',
        transfer_date: new Date().toISOString().split('T')[0],
        reason: '',
        notes: '',
    });
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await transfersAPI.create(formData);
            onSuccess();
        } catch (error) {
            alert('Failed to create transfer: ' + (error.response?.data?.detail || error.message));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-6 max-w-2xl w-full">
                <h3 className="text-2xl font-bold mb-4">New Transfer</h3>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Asset ID *</label>
                            <input
                                type="number"
                                required
                                value={formData.asset_id}
                                onChange={(e) => setFormData({ ...formData, asset_id: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">From Unit ID *</label>
                            <input
                                type="number"
                                required
                                value={formData.from_unit_id}
                                onChange={(e) => setFormData({ ...formData, from_unit_id: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">To Unit ID *</label>
                            <input
                                type="number"
                                required
                                value={formData.to_unit_id}
                                onChange={(e) => setFormData({ ...formData, to_unit_id: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Quantity *</label>
                            <input
                                type="number"
                                required
                                value={formData.quantity}
                                onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                        <div className="col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Transfer Date *</label>
                            <input
                                type="date"
                                required
                                value={formData.transfer_date}
                                onChange={(e) => setFormData({ ...formData, transfer_date: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Reason</label>
                        <input
                            type="text"
                            value={formData.reason}
                            onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Notes</label>
                        <textarea
                            value={formData.notes}
                            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            rows="3"
                        />
                    </div>
                    <div className="flex gap-4">
                        <button
                            type="submit"
                            disabled={loading}
                            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg disabled:opacity-50"
                        >
                            {loading ? 'Creating...' : 'Create Transfer'}
                        </button>
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 rounded-lg"
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Transfers;
