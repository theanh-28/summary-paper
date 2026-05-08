import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

/**
 * Route guard cho các trang chỉ admin mới truy cập được.
 * Redirect về / nếu user không phải admin.
 * Redirect về /login nếu chưa đăng nhập.
 */
function AdminRoute({ children }) {
    const { token, isAdmin } = useContext(AuthContext);

    if (!token) return <Navigate to="/login" />;
    if (!isAdmin()) return <Navigate to="/" />;

    return children;
}

export default AdminRoute;
