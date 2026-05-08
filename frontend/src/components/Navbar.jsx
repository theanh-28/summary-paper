import { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Navbar() {
    const { token, user, logout, isAdmin } = useContext(AuthContext);

    if (!token) return null;

    return (
        <nav className="navbar" id="main-navbar">
            <h2>AI Summary Paper</h2>
            <div className="links">
                <Link to="/">Tạo Tóm Tắt</Link>
                <Link to="/history">Lịch Sử</Link>
                <Link to="/dashboard">Dashboard</Link>
                {isAdmin() && (
                    <Link to="/admin" className="admin-link">
                        ⚙️ Admin
                    </Link>
                )}
                <span className="user-badge">
                    {user?.role === 'admin' ? '👑' : '👤'} {user?.role}
                </span>
                <button onClick={logout} className="logout-btn">Đăng xuất</button>
            </div>
        </nav>
    );
}

export default Navbar;
