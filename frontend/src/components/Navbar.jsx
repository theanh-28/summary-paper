import { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Navbar() {
    const { token, logout } = useContext(AuthContext);

    if (!token) return null;

    return (
        <nav className="navbar">
            <h2>AI Summary Paper</h2>
            <div className="links">
                <Link to="/">Tạo Tóm Tắt</Link>
                <Link to="/history">Lịch Sử</Link>
                <button onClick={logout} className="logout-btn">Đăng xuất</button>
            </div>
        </nav>
    );
}

export default Navbar;
