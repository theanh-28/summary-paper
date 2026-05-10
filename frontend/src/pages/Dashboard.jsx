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
    const [token, setToken] = useState(null);
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
                if (res.data.token) {
                    setToken(res.data.token);
                    
                    // Lấy base URL của Metabase từ embed_url
                    const metabaseSiteUrl = new URL(res.data.embed_url).origin;
                    
                    // Cấu hình Metabase
                    window.metabaseConfig = {
                        theme: { preset: "dark" },
                        isGuest: true,
                        instanceUrl: metabaseSiteUrl
                    };
                    
                    // Tải script nhúng (embed.js) của Metabase nếu chưa có
                    if (!document.getElementById('metabase-embed-script')) {
                        const script = document.createElement('script');
                        script.id = 'metabase-embed-script';
                        script.src = `${metabaseSiteUrl}/app/embed.js`;
                        script.defer = true;
                        document.body.appendChild(script);
                    }
                }
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
                    {token ? (
                        <div style={{ padding: '1rem', background: '#000', borderRadius: '16px' }}>
                            <metabase-dashboard 
                                token={token} 
                                with-title="true" 
                                with-downloads="true"
                            ></metabase-dashboard>
                        </div>
                    ) : (
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
                    )}
                </div>
            )}
        </div>
    );
}

export default Dashboard;
