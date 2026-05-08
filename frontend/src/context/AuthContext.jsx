import { createContext, useState, useEffect } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [user, setUser] = useState(null);
    const [loadingAuth, setLoadingAuth] = useState(true);
    const navigate = useNavigate();

    const fetchUserProfile = async (currentToken) => {
        try {
            // Fetch directly with standard axios instead of interceptor to prevent loop issues if any,
            // but `api.get` is fine here because interceptors handle the token.
            const res = await api.get('/users/me', {
                headers: { Authorization: `Bearer ${currentToken}` }
            });
            setUser(res.data);
        } catch (err) {
            console.error('Failed to fetch user profile:', err);
            if (err.response?.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('token');
                setToken(null);
                setUser(null);
            }
        } finally {
            setLoadingAuth(false);
        }
    };

    useEffect(() => {
        if (token) {
            fetchUserProfile(token);
        } else {
            setLoadingAuth(false);
        }
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    const login = async (email, password) => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const res = await api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        const newToken = res.data.access_token;
        localStorage.setItem('token', newToken);
        setToken(newToken);
        
        await fetchUserProfile(newToken);
        navigate('/');
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        navigate('/login');
    };

    const updateProfileData = (newData) => {
        setUser((prev) => ({ ...prev, ...newData }));
    };

    const isAdmin = () => ['admin', 'root'].includes(user?.role);

    return (
        <AuthContext.Provider value={{ token, user, login, logout, isAdmin, loadingAuth, updateProfileData }}>
            {!loadingAuth ? children : <div className="dashboard-loading"><div className="spinner"></div></div>}
        </AuthContext.Provider>
    );
};
