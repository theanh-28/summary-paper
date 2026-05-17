import { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

function Profile() {
    const { user, updateProfileData } = useContext(AuthContext);
    const [fullName, setFullName] = useState('');
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    
    const [profileLoading, setProfileLoading] = useState(false);
    const [passwordLoading, setPasswordLoading] = useState(false);
    const [profileMsg, setProfileMsg] = useState({ text: '', type: '' });
    const [passwordMsg, setPasswordMsg] = useState({ text: '', type: '' });

    useEffect(() => {
        if (user) {
            setFullName(user.full_name || '');
        }
    }, [user]);

    const handleUpdateProfile = async (e) => {
        e.preventDefault();
        setProfileMsg({ text: '', type: '' });
        setProfileLoading(true);
        try {
            const res = await api.put('/users/me', { full_name: fullName });
            updateProfileData({ full_name: res.data.full_name });
            setProfileMsg({ text: 'Cập nhật hồ sơ thành công!', type: 'success' });
            setTimeout(() => setProfileMsg({ text: '', type: '' }), 3000);
        } catch (err) {
            setProfileMsg({ text: err.response?.data?.detail || 'Lỗi khi cập nhật hồ sơ', type: 'error' });
        } finally {
            setProfileLoading(false);
        }
    };

    const handleChangePassword = async (e) => {
        e.preventDefault();
        setPasswordMsg({ text: '', type: '' });
        if (newPassword !== confirmPassword) {
            setPasswordMsg({ text: 'Mật khẩu xác nhận không khớp', type: 'error' });
            return;
        }
        setPasswordLoading(true);
        try {
            const res = await api.put('/users/me/change-password', {
                current_password: currentPassword,
                new_password: newPassword,
                confirm_password: confirmPassword
            });
            setPasswordMsg({ text: res.data.detail || 'Đổi mật khẩu thành công!', type: 'success' });
            setCurrentPassword('');
            setNewPassword('');
            setConfirmPassword('');
            setTimeout(() => setPasswordMsg({ text: '', type: '' }), 3000);
        } catch (err) {
            setPasswordMsg({ text: err.response?.data?.detail || 'Lỗi khi đổi mật khẩu', type: 'error' });
        } finally {
            setPasswordLoading(false);
        }
    };

    if (!user) return null;

    const displayRoleIcon = user.role === 'root' ? '👑' : user.role === 'admin' ? '🛡️' : '👤';
    const roleName = user.role === 'root' ? 'Tài khoản Root' : user.role === 'admin' ? 'Quản trị viên' : 'Người dùng tiêu chuẩn';

    return (
        <div className="profile-container">
            <div className="profile-header">
                <h2>Hồ Sơ Tài Khoản</h2>
                <p>Quản lý thông tin cá nhân và bảo mật</p>
            </div>

            <div className="profile-grid">
                {/* Thông tin cơ bản */}
                <div className="glass-card">
                    <h3>Thông Tin Chung</h3>
                    <div className="profile-info-display">
                        <div className="info-group">
                            <span className="info-label">Email đăng nhập</span>
                            <span className="info-value">{user.email}</span>
                        </div>
                        <div className="info-group">
                            <span className="info-label">Cấp độ tài khoản</span>
                            <span className="info-value" style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                                {displayRoleIcon} {roleName}
                            </span>
                        </div>
                        <div className="info-group">
                            <span className="info-label">Trạng thái</span>
                            <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                                {user.is_active ? '✅ Đang hoạt động' : '🚫 Vô hiệu hóa'}
                            </span>
                        </div>
                        <div className="info-group">
                            <span className="info-label">Ngày tham gia</span>
                            <span className="info-value">{new Date(user.created_at).toLocaleDateString('vi-VN')}</span>
                        </div>
                    </div>
                </div>

                {/* Chỉnh sửa hồ sơ */}
                <div className="glass-card">
                    <h3>Cập Nhật Hồ Sơ</h3>
                    <form onSubmit={handleUpdateProfile} className="profile-form">
                        <div className="form-group">
                            <label>Tên hiển thị</label>
                            <input 
                                type="text" 
                                value={fullName} 
                                onChange={e => setFullName(e.target.value)} 
                                placeholder="Nhập tên hiển thị của bạn..."
                                required
                            />
                        </div>
                        {profileMsg.text && (
                            <div className={`msg-alert ${profileMsg.type}`}>
                                {profileMsg.text}
                            </div>
                        )}
                        <button type="submit" disabled={profileLoading} className="btn-primary">
                            {profileLoading ? 'Đang lưu...' : 'Lưu Thay Đổi'}
                        </button>
                    </form>
                </div>

                {/* Đổi mật khẩu */}
                <div className="glass-card">
                    <h3>Đổi Mật Khẩu</h3>
                    <form onSubmit={handleChangePassword} className="profile-form">
                        <div className="form-group">
                            <label>Mật khẩu hiện tại</label>
                            <input 
                                type="password" 
                                value={currentPassword} 
                                onChange={e => setCurrentPassword(e.target.value)} 
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Mật khẩu mới</label>
                            <input 
                                type="password" 
                                value={newPassword} 
                                onChange={e => setNewPassword(e.target.value)} 
                                minLength={8}
                                placeholder="Ít nhất 8 ký tự"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Xác nhận mật khẩu mới</label>
                            <input 
                                type="password" 
                                value={confirmPassword} 
                                onChange={e => setConfirmPassword(e.target.value)} 
                                minLength={8}
                                required
                            />
                        </div>
                        {passwordMsg.text && (
                            <div className={`msg-alert ${passwordMsg.type}`}>
                                {passwordMsg.text}
                            </div>
                        )}
                        <button type="submit" disabled={passwordLoading} className="btn-primary">
                            {passwordLoading ? 'Đang xử lý...' : 'Cập Nhật Mật Khẩu'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Profile;
