import { useState, useEffect } from 'react';
import { purchasesAPI } from '../services/api';

function Purchases() {
    const [purchases, setPurchases] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [filters, setFilters] = useState({
        unit_id: '',
        category_id: '',
        start_date: '',
        end_date: '',
    });

    useEffect(() => {
        fetchPurchases();
    }, []);

    const fetchPurchases = async () => {
        setLoading(true);
        try {
            const params = {};
            if (filters.unit_id) params.unit_id = filters.unit_id;
            if (filters.category_id) params.category_id = filters.category_id;
            if (filters.start_date) params.start_date = filters.start_date;
            if (filters.end_date) params.end_date = filters.end_date;

            const response = await purchasesAPI.list(params);
            setPurchases(response.data);
        } catch (error) {
            console.error('Failed to fetch purchases:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleFilterChange = (e) => {
        setFilters({ ...filters, [e.target.name]: e.target.value });
    };

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Purchases</h1>
                <button
                    onClick={() => setShowForm(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                >
                    + New Purchase
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
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                    </div>
                </div>
                <button
                    onClick={fetchPurchases}
                    className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                >
                    Apply Filters
                </button>
            </div>

            {/* Purchases Table */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Asset ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Unit ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Unit Price</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
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
                        ) : purchases.length === 0 ? (
                            <tr>
                                <td colSpan="7" className="px-6 py-4 text-center text-gray-500">
                                    No purchases found
                                </td>
                            </tr>
                        ) : (
                            purchases.map((purchase) => (
                                <tr key={purchase.id} className="hover:bg-gray-50">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{purchase.id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{purchase.asset_id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{purchase.unit_id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{purchase.quantity}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${purchase.unit_price}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                                        ${purchase.total_amount}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                        {new Date(purchase.purchase_date).toLocaleDateString()}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* New Purchase Form Modal */}
            {showForm && (
                <PurchaseForm
                    onClose={() => setShowForm(false)}
                    onSuccess={() => {
                        setShowForm(false);
                        fetchPurchases();
                    }}
                />
            )}
        </div>
    );
}

function PurchaseForm({ onClose, onSuccess }) {
    const [formData, setFormData] = useState({
        asset_id: '',
        unit_id: '',
        category_id: '',
        quantity: '',
        unit_price: '',
        purchase_date: new Date().toISOString().split('T')[0],
        vendor: '',
        invoice_number: '',
        notes: '',
    });
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await purchasesAPI.create(formData);
            onSuccess();
        } catch (error) {
            alert('Failed to create purchase: ' + (error.response?.data?.detail || error.message));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <h3 className="text-2xl font-bold mb-4">New Purchase</h3>
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
                            <label className="block text-sm font-medium text-gray-700 mb-2">Unit ID *</label>
                            <input
                                type="number"
                                required
                                value={formData.unit_id}
                                onChange={(e) => setFormData({ ...formData, unit_id: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Category ID *</label>
                            <input
                                type="number"
                                required
                                value={formData.category_id}
                                onChange={(e) => setFormData({ ...formData, category_id: e.target.value })}
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
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Unit Price *</label>
                            <input
                                type="number"
                                step="0.01"
                                required
                                value={formData.unit_price}
                                onChange={(e) => setFormData({ ...formData, unit_price: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Purchase Date *</label>
                            <input
                                type="date"
                                required
                                value={formData.purchase_date}
                                onChange={(e) => setFormData({ ...formData, purchase_date: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Vendor</label>
                            <input
                                type="text"
                                value={formData.vendor}
                                onChange={(e) => setFormData({ ...formData, vendor: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Invoice Number</label>
                            <input
                                type="text"
                                value={formData.invoice_number}
                                onChange={(e) => setFormData({ ...formData, invoice_number: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            />
                        </div>
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
                            {loading ? 'Creating...' : 'Create Purchase'}
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

export default Purchases;
