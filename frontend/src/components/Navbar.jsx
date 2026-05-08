import { useContext, useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Navbar() {
    const { token, user, logout, isAdmin } = useContext(AuthContext);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        function handleClickOutside(event) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    if (!token) return null;

    const displayRoleIcon = user?.role === 'root' ? '👑' : user?.role === 'admin' ? '🛡️' : '👤';
    const displayName = user?.full_name || user?.email?.split('@')[0] || 'User';

    return (
        <nav className="navbar" id="main-navbar">
            <h2>AI Summary Paper</h2>
            <div className="links">
                <Link to="/">Tạo Tóm Tắt</Link>
                <Link to="/history">Lịch Sử</Link>
                
                <div className="account-menu" ref={dropdownRef}>
                    <button 
                        className="account-btn" 
                        onClick={() => setDropdownOpen(!dropdownOpen)}
                    >
                        <span className="account-avatar">{displayRoleIcon}</span>
                        <span className="account-name">{displayName}</span>
                        <span className="account-arrow">▼</span>
                    </button>
                    
                    {dropdownOpen && (
                        <div className="account-dropdown">
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
        </nav>
    );
}

export default Navbar;
