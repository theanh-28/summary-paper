import { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Login() {
    const { login } = useContext(AuthContext);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(email, password);
        } catch (err) {
            setError('Đăng nhập thất bại. Vui lòng kiểm tra lại email/password.');
        }
    };

    return (
        <div className="login-container">
            <div className="glass-card login-form">
                <h2>Welcome Back</h2>
                <p style={{textAlign: 'center', marginBottom: '2rem', color: 'var(--text-muted)'}}>Đăng nhập để tóm tắt bài báo</p>
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
                        placeholder="Mật khẩu" 
                        value={password} 
                        onChange={e => setPassword(e.target.value)} 
                        required 
                    />
                    <button type="submit">Đăng Nhập</button>
                </form>
                <div style={{textAlign: 'center', marginTop: '1.5rem'}}>
                    <Link to="/register" style={{color: 'var(--primary)', textDecoration: 'none'}}>Chưa có tài khoản? Đăng ký ngay</Link>
                </div>
            </div>
        </div>
    );
}

export default Login;
