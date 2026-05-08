import { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Login() {
    const { login } = useContext(AuthContext);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await login(email, password);
        } catch (err) {
            setError(err.response?.data?.detail || 'Đăng nhập thất bại. Vui lòng kiểm tra lại email/password.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container" id="login-page">
            <div className="glass-card login-form">
                <h2>Welcome Back</h2>
                <p style={{textAlign: 'center', marginBottom: '2rem', color: 'var(--text-muted)'}}>Đăng nhập để tóm tắt bài báo</p>
                {error && <p className="error" id="login-error">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <input
                        id="login-email"
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        required
                        autoComplete="email"
                    />
                    <input
                        id="login-password"
                        type="password"
                        placeholder="Mật khẩu"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        required
                        autoComplete="current-password"
                    />
                    <button type="submit" id="login-submit" disabled={loading}>
                        {loading ? 'Đang đăng nhập...' : 'Đăng Nhập'}
                    </button>
                </form>
                <div style={{textAlign: 'center', marginTop: '1.5rem'}}>
                    <Link to="/register" style={{color: 'var(--primary)', textDecoration: 'none'}}>Chưa có tài khoản? Đăng ký ngay</Link>
                </div>
            </div>
        </div>
    );
}

export default Login;
