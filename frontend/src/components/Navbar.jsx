import { useContext, useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

function Navbar() {
    const { token, user, logout, isAdmin } = useContext(AuthContext);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [historyExpanded, setHistoryExpanded] = useState(true);
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);
    const [papers, setPapers] = useState([]);
    const dropdownRef = useRef(null);
    const location = useLocation();

    useEffect(() => {
        function handleClickOutside(event) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        }
        document.addEventListener('mousedown', handleClickOutside);
        
        if (token) {
            api.get('/papers/')
               .then(res => setPapers(res.data))
               .catch(err => console.error(err));
        }

        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [token, location.pathname]); // Refresh history if navigation happens

    // Đóng mobile sidebar khi navigate
    useEffect(() => {
        setMobileOpen(false);
    }, [location.pathname]);

    if (!token) return null;

    const displayRoleIcon = user?.role === 'root' ? '👑' : user?.role === 'admin' ? '🛡️' : '👤';
    const displayName = user?.full_name || user?.email?.split('@')[0] || 'User';

    // Status icon helpers
    const getStatusIcon = (status) => {
        switch (status) {
            case 'processing': return '⏳';
            case 'completed': return '✅';
            case 'failed': return '❌';
            default: return '📄';
        }
    };

    const sidebarClasses = [
        'sidebar',
        sidebarCollapsed ? 'sidebar-collapsed' : '',
        mobileOpen ? 'sidebar-mobile-open' : '',
    ].filter(Boolean).join(' ');

    return (
        <>
            {/* Mobile hamburger button */}
            <button 
                className="mobile-menu-btn"
                onClick={() => setMobileOpen(!mobileOpen)}
                aria-label="Toggle menu"
            >
                {mobileOpen ? '✕' : '☰'}
            </button>

            {/* Mobile overlay */}
            {mobileOpen && (
                <div 
                    className="sidebar-overlay" 
                    onClick={() => setMobileOpen(false)} 
                />
            )}

            <aside className={sidebarClasses} id="main-sidebar">
                <div className="sidebar-header">
                    {!sidebarCollapsed && <h2>AI Summary</h2>}
                    <button 
                        className="sidebar-toggle-btn"
                        onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
                        title={sidebarCollapsed ? 'Mở rộng' : 'Thu gọn'}
                    >
                        {sidebarCollapsed ? '»' : '«'}
                    </button>
                </div>
                
                <div className="sidebar-nav">
                    <Link to="/" className="sidebar-link" title="Tạo Tóm Tắt">
                        <span className="sidebar-icon">✍️</span>
                        {!sidebarCollapsed && <span>Tạo Tóm Tắt</span>}
                    </Link>
                    
                    {!sidebarCollapsed && (
                        <div className="sidebar-section">
                            <button 
                                className="sidebar-section-title"
                                onClick={() => setHistoryExpanded(!historyExpanded)}
                            >
                                <span>Gần đây</span>
                                <span className={`section-arrow ${historyExpanded ? 'expanded' : ''}`}>›</span>
                            </button>
                            {historyExpanded && (
                                <div className="sidebar-history-list">
                                    {papers.length > 0 ? papers.map(p => (
                                        <Link 
                                            key={p.id} 
                                            to={`/paper/${p.id}`} 
                                            className={`sidebar-history-item ${location.pathname === `/paper/${p.id}` ? 'active' : ''}`}
                                            title={`${p.title} (${p.status})`}
                                        >
                                            <span className="history-status-icon">{getStatusIcon(p.status)}</span>
                                            <span className="history-title">{p.title}</span>
                                        </Link>
                                    )) : (
                                        <div className="sidebar-empty">Chưa có bài báo nào</div>
                                    )}
                                </div>
                            )}
                        </div>
                    )}
                </div>
                
                <div className="sidebar-footer">
                    <div className="account-menu" ref={dropdownRef}>
                        <button 
                            className="account-btn" 
                            onClick={() => setDropdownOpen(!dropdownOpen)}
                            title={displayName}
                        >
                            <span className="account-avatar">{displayRoleIcon}</span>
                            {!sidebarCollapsed && (
                                <>
                                    <span className="account-name">{displayName}</span>
                                    <span className="account-arrow">{dropdownOpen ? '▲' : '▼'}</span>
                                </>
                            )}
                        </button>
                        
                        {dropdownOpen && (
                            <div className="account-dropdown sidebar-dropdown">
                                <div className="dropdown-header">
                                    <strong>{displayName}</strong>
                                    <span>{user?.email}</span>
                                </div>
                                <hr className="dropdown-divider" />
                                <Link to="/profile" className="dropdown-item" onClick={() => setDropdownOpen(false)}>
                                    👤 Hồ sơ tài khoản
                                </Link>
                                <Link to="/dashboard" className="dropdown-item" onClick={() => setDropdownOpen(false)}>
                                    📈 Dashboard
                                </Link>
                                <Link to="/guide" className="dropdown-item" onClick={() => setDropdownOpen(false)}>
                                    📖 Hướng dẫn sử dụng
                                </Link>
                                {isAdmin() && (
                                    <Link to="/admin" className="dropdown-item admin-item" onClick={() => setDropdownOpen(false)}>
                                        ⚙️ Quản trị hệ thống
                                    </Link>
                                )}
                                <hr className="dropdown-divider" />
                                <button onClick={logout} className="dropdown-item text-danger">
                                    🚪 Đăng xuất
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </aside>
        </>
    );
}

export default Navbar;
