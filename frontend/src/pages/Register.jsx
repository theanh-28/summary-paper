import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

function Register() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await api.post('/auth/register', { email, password });
            // Đăng ký thành công thì chuyển về trang login
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.detail || 'Đăng ký thất bại. Email có thể đã tồn tại.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="glass-card login-form">
                <h2>Tạo Tài Khoản</h2>
                <p style={{textAlign: 'center', marginBottom: '2rem', color: 'var(--text-muted)'}}>Đăng ký để bắt đầu sử dụng AI</p>
                {error && <p className="error">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <input 
                        type="email" 
                        placeholder="Email" 
                        value={email} 
                        onChange={e => setEmail(e.target.value)} 
                        required 
                    />
                    <input 
                        type="password" 
                        placeholder="Mật khẩu (ít nhất 8 ký tự)" 
                        value={password} 
                        onChange={e => setPassword(e.target.value)} 
                        required 
                        minLength={8}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? 'Đang xử lý...' : 'Đăng Ký'}
                    </button>
                </form>
                <div style={{textAlign: 'center', marginTop: '1.5rem'}}>
                    <Link to="/login" style={{color: 'var(--primary)', textDecoration: 'none'}}>Đã có tài khoản? Đăng nhập ngay</Link>
                </div>
            </div>
        </div>
    );
}

export default Register;
