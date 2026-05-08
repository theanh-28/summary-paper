import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

/**
 * Route guard cho các trang yêu cầu đăng nhập.
 * Redirect về /login nếu chưa có token.
 */
function PrivateRoute({ children }) {
    const { token } = useContext(AuthContext);
    return token ? children : <Navigate to="/login" />;
}

export default PrivateRoute;
