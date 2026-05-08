import { useState, useEffect } from 'react';
import api from '../services/api';

/**
 * Admin Dashboard — quản lý user, xem thống kê hệ thống.
 * Chỉ accessible qua AdminRoute (kiểm tra role=admin).
 */
function AdminDashboard() {
    const [stats, setStats] = useState(null);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [actionLoading, setActionLoading] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [statsRes, usersRes] = await Promise.all([
                api.get('/admin/stats'),
                api.get('/admin/users?limit=100'),
            ]);
            setStats(statsRes.data);
            setUsers(usersRes.data);
        } catch (err) {
            setError('Không thể tải dữ liệu admin. Kiểm tra quyền truy cập.');
        } finally {
            setLoading(false);
        }
    };

    const handleToggleActive = async (userId) => {
        setActionLoading(userId);
        try {
            await api.put(`/admin/users/${userId}/toggle-active`);
            await fetchData();
        } catch (err) {
            alert(err.response?.data?.detail || 'Lỗi khi thay đổi trạng thái user');
        } finally {
            setActionLoading(null);
        }
    };

    const handleChangeRole = async (userId, newRole) => {
        setActionLoading(userId);
        try {
            await api.put(`/admin/users/${userId}/role`, { role: newRole });
            await fetchData();
        } catch (err) {
            alert(err.response?.data?.detail || 'Lỗi khi thay đổi role');
        } finally {
            setActionLoading(null);
        }
    };

    const handleDeleteUser = async (userId, email) => {
        if (!confirm(`Bạn chắc chắn muốn xóa user "${email}"?`)) return;
        setActionLoading(userId);
        try {
            await api.delete(`/admin/users/${userId}`);
            await fetchData();
        } catch (err) {
            alert(err.response?.data?.detail || 'Lỗi khi xóa user');
        } finally {
            setActionLoading(null);
        }
    };

    if (loading) {
        return (
            <div style={{ textAlign: 'center', marginTop: '5rem' }}>
                <div className="spinner"></div>
                <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Đang tải admin panel...</p>
            </div>
        );
    }

    if (error) {
        return <div className="glass-card error">{error}</div>;
    }

    return (
        <div className="admin-container" id="admin-dashboard">
            <h2 style={{ marginBottom: '2rem' }}>⚙️ Quản Trị Hệ Thống</h2>

            {/* Stats Cards */}
            {stats && (
                <div className="stats-grid">
                    <div className="stat-card glass-card">
                        <div className="stat-icon">👥</div>
                        <div className="stat-value">{stats.total_users}</div>
                        <div className="stat-label">Tổng User</div>
                    </div>
                    <div className="stat-card glass-card">
                        <div className="stat-icon">📄</div>
                        <div className="stat-value">{stats.total_papers}</div>
                        <div className="stat-label">Tổng Papers</div>
                    </div>
                    <div className="stat-card glass-card">
                        <div className="stat-icon">📝</div>
                        <div className="stat-value">{stats.total_summaries}</div>
                        <div className="stat-label">Tổng Summaries</div>
                    </div>
                </div>
            )}

            {/* Users Table */}
            <div className="glass-card" style={{ marginTop: '2rem' }}>
                <h3 style={{ marginBottom: '1.5rem' }}>Quản lý User ({users.length})</h3>
                <div className="users-table-wrapper">
                    <table className="users-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Email</th>
                                <th>Role</th>
                                <th>Trạng thái</th>
                                <th>Ngày tạo</th>
                                <th>Hành động</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map(u => (
                                <tr key={u.id} className={!u.is_active ? 'inactive-row' : ''}>
                                    <td>{u.id}</td>
                                    <td>{u.email}</td>
                                    <td>
                                        <span className={`role-badge role-${u.role}`}>
                                            {u.role === 'admin' ? '👑 Admin' : '👤 User'}
                                        </span>
                                    </td>
                                    <td>
                                        <span className={`status-badge ${u.is_active ? 'active' : 'inactive'}`}>
                                            {u.is_active ? '✅ Active' : '🚫 Inactive'}
                                        </span>
                                    </td>
                                    <td>{new Date(u.created_at).toLocaleDateString('vi-VN')}</td>
                                    <td className="action-buttons">
                                        <button
                                            className="btn-action btn-toggle"
                                            onClick={() => handleToggleActive(u.id)}
                                            disabled={actionLoading === u.id}
                                            title={u.is_active ? 'Vô hiệu hóa' : 'Kích hoạt'}
                                        >
                                            {u.is_active ? '🔒' : '🔓'}
                                        </button>
                                        <button
                                            className="btn-action btn-role"
                                            onClick={() => handleChangeRole(u.id, u.role === 'admin' ? 'user' : 'admin')}
                                            disabled={actionLoading === u.id}
                                            title={u.role === 'admin' ? 'Hạ quyền' : 'Nâng quyền Admin'}
                                        >
                                            {u.role === 'admin' ? '⬇️' : '⬆️'}
                                        </button>
                                        <button
                                            className="btn-action btn-delete"
                                            onClick={() => handleDeleteUser(u.id, u.email)}
                                            disabled={actionLoading === u.id}
                                            title="Xóa user"
                                        >
                                            🗑️
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default AdminDashboard;
