import { createContext, useState, useEffect } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

/**
 * Decode JWT payload (phần giữa của token) để lấy thông tin user.
 * Không verify signature — chỉ đọc claims để hiển thị UI.
 * Backend luôn verify signature khi xử lý request.
 */
function decodeJwtPayload(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
            atob(base64)
                .split('')
                .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        );
        return JSON.parse(jsonPayload);
    } catch {
        return null;
    }
}

/**
 * Lấy thông tin user từ token JWT.
 */
function getUserFromToken(token) {
    if (!token) return null;
    const payload = decodeJwtPayload(token);
    if (!payload) return null;
    return {
        id: parseInt(payload.sub),
        role: payload.role || 'user',
    };
}

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [user, setUser] = useState(() => {
        const savedToken = localStorage.getItem('token');
        return getUserFromToken(savedToken);
    });
    const navigate = useNavigate();

    // Kiểm tra token expiry khi khởi tạo
    useEffect(() => {
        if (token) {
            const payload = decodeJwtPayload(token);
            if (payload && payload.exp * 1000 < Date.now()) {
                // Token đã hết hạn
                logout();
            }
        }
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    const login = async (email, password) => {
        const formData = new URLSearchParams();
        formData.append('username', email); // OAuth2 form
        formData.append('password', password);

        const res = await api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        const newToken = res.data.access_token;
        localStorage.setItem('token', newToken);
        setToken(newToken);

        const userInfo = getUserFromToken(newToken);
        setUser(userInfo);

        navigate('/');
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        navigate('/login');
    };

    /**
     * Kiểm tra user hiện tại có phải admin không.
     */
    const isAdmin = () => user?.role === 'admin';

    return (
        <AuthContext.Provider value={{ token, user, login, logout, isAdmin }}>
            {children}
        </AuthContext.Provider>
    );
};
