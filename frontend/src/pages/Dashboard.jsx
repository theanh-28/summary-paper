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
        
        // CSS hack to remove padding for full width dashboard
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.style.padding = '0';
            mainContent.style.maxWidth = 'none';
        }
        return () => {
            if (mainContent) {
                mainContent.style.padding = '';
                mainContent.style.maxWidth = '';
            }
        };
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
                        theme: { preset: "light" }, // Cập nhật sang giao diện sáng
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
        <div className="dashboard-container" id="dashboard-page" style={{ height: '100%', width: '100%', display: 'flex', flexDirection: 'column' }}>
            {error ? (
                <div className="glass-card" style={{ textAlign: 'center', margin: '2rem' }}>
                    <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>
                        ⚠️ {error}
                    </p>
                    <p style={{ color: 'var(--text-muted)', marginTop: '1rem', fontSize: '0.9rem' }}>
                        Hãy cấu hình Metabase và set <code>METABASE_SECRET_KEY</code> trong file .env
                    </p>
                </div>
            ) : (
                <div style={{ flex: 1, overflow: 'hidden', height: '100vh' }}>
                    {token ? (
                        <metabase-dashboard 
                            token={token} 
                            with-downloads="true"
                            style={{ width: '100%', height: '100%', display: 'block' }}
                        ></metabase-dashboard>
                    ) : (
                        <iframe
                            title="Metabase Dashboard"
                            src={embedUrl}
                            width="100%"
                            height="100%"
                            frameBorder="0"
                            allowFullScreen={true}
                            style={{
                                border: 'none',
                                display: 'block',
                                width: '100%',
                                height: '100%'
                            }}
                        ></iframe>
                    )}
                </div>
            )}
        </div>
    );
}

export default Dashboard;
