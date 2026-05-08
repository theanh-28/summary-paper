import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

/**
 * Dashboard page — hiển thị Metabase embedded dashboard
 * tùy theo role của user (admin/user).
 */
function Dashboard() {
    const { user } = useContext(AuthContext);
    const [embedUrl, setEmbedUrl] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchEmbedUrl();
    }, []);

    const fetchEmbedUrl = async () => {
        try {
            const res = await api.get('/dashboard/embed-url');
            if (res.data.embed_url) {
                setEmbedUrl(res.data.embed_url);
            } else {
                setError(res.data.message || 'Metabase chưa được cấu hình.');
            }
        } catch (err) {
            console.error('Error fetching embed URL:', err);
            setError('Không thể tải dashboard. Vui lòng thử lại sau.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="dashboard-loading">
                <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <div className="spinner"></div>
                    <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Đang tải dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="dashboard-container" id="dashboard-page">
            <div className="dashboard-header">
                <h2 style={{ marginBottom: '0.5rem' }}>
                    {['admin', 'root'].includes(user?.role) ? '📊 Admin Dashboard' : '📈 Dashboard Cá Nhân'}
                </h2>
                <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
                    {['admin', 'root'].includes(user?.role)
                        ? 'Tổng quan hệ thống — analytics toàn bộ dữ liệu'
                        : 'Dữ liệu và thống kê của bạn'}
                </p>
            </div>

            {error ? (
                <div className="glass-card" style={{ textAlign: 'center' }}>
                    <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>
                        ⚠️ {error}
                    </p>
                    <p style={{ color: 'var(--text-muted)', marginTop: '1rem', fontSize: '0.9rem' }}>
                        Hãy cấu hình Metabase và set <code>METABASE_SECRET_KEY</code> trong file .env
                    </p>
                </div>
            ) : (
                <div className="glass-card" style={{ padding: '0', overflow: 'hidden' }}>
                    <iframe
                        title="Metabase Dashboard"
                        src={embedUrl}
                        width="100%"
                        height="800"
                        frameBorder="0"
                        allowFullScreen={true}
                        style={{
                            border: 'none',
                            borderRadius: '16px',
                            display: 'block',
                        }}
                    ></iframe>
                </div>
            )}
        </div>
    );
}

export default Dashboard;
