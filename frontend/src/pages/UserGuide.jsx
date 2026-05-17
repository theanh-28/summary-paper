import { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';

function UserGuide() {
    const { user, isAdmin } = useContext(AuthContext);
    const [activeTab, setActiveTab] = useState('user');

    if (!user) return null;

    const showAdminTab = isAdmin();

    return (
        <div className="guide-container">
            <div className="guide-header">
                <h2>📖 Hướng Dẫn Sử Dụng</h2>
                <p>Tìm hiểu cách sử dụng AI Summary một cách hiệu quả nhất</p>
            </div>

            {/* Tab navigation - chỉ hiện tab Admin nếu user là admin/root */}
            <div className="guide-tabs">
                <button
                    className={`guide-tab ${activeTab === 'user' ? 'active' : ''}`}
                    onClick={() => setActiveTab('user')}
                >
                    👤 Người dùng
                </button>
                {showAdminTab && (
                    <button
                        className={`guide-tab ${activeTab === 'admin' ? 'active' : ''}`}
                        onClick={() => setActiveTab('admin')}
                    >
                        🛡️ Quản trị viên
                    </button>
                )}
            </div>

            {/* === NỘI DUNG CHO NGƯỜI DÙNG THƯỜNG === */}
            {activeTab === 'user' && (
                <div className="guide-content">
                    {/* 1. Tổng quan */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">🎯</div>
                        <h3>Tổng quan</h3>
                        <p>
                            <strong>AI Summary</strong> tự động tóm tắt bài báo khoa học bằng AI. Chỉ cần tải file lên, bạn sẽ nhận được bản tóm tắt tiếng Việt ngắn gọn.
                        </p>
                        <div className="guide-highlight">
                            💡 Định dạng hỗ trợ: <strong>PDF</strong>, <strong>DOCX</strong> và <strong>TXT</strong>
                        </div>
                    </div>

                    {/* 2. Upload & Tóm tắt */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">📤</div>
                        <h3>1. Tạo tóm tắt</h3>
                        <ol className="guide-steps">
                            <li>Nhấn <strong>✍️ Tạo Tóm Tắt</strong> ở menu trái.</li>
                            <li>Nhập tiêu đề và chọn file đính kèm.</li>
                            <li>Nhấn <strong>Tải lên & Tóm tắt</strong>.</li>
                        </ol>
                        <div className="guide-note">
                            ⏳ Quá trình xử lý mất <strong>30s – 3 phút</strong>. Hệ thống chạy ngầm nên bạn có thể làm việc khác trong lúc chờ.
                        </div>
                    </div>

                    {/* 3. Xem kết quả */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">📋</div>
                        <h3>2. Xem kết quả</h3>
                        <ol className="guide-steps">
                            <li>Chờ trạng thái bài báo chuyển thành <span className="status-pill status-completed">✅ Hoàn tất</span>.</li>
                            <li>Chọn bài báo ở mục <strong>"Gần đây"</strong> (menu trái) để đọc bản tóm tắt chi tiết.</li>
                        </ol>
                    </div>

                    {/* 4. Trạng thái bài báo */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">🔄</div>
                        <h3>Các trạng thái</h3>
                        <div className="guide-status-grid">
                            <div className="guide-status-item">
                                <span className="status-pill status-uploaded">📄 Đã tải</span>
                                <span>File đã lên hệ thống, chờ xếp hàng</span>
                            </div>
                            <div className="guide-status-item">
                                <span className="status-pill status-processing">⏳ Đang xử lý</span>
                                <span>AI đang đọc và tóm tắt nội dung</span>
                            </div>
                            <div className="guide-status-item">
                                <span className="status-pill status-completed">✅ Hoàn tất</span>
                                <span>Bản tóm tắt đã sẵn sàng</span>
                            </div>
                            <div className="guide-status-item">
                                <span className="status-pill status-failed">❌ Lỗi</span>
                                <span>Xử lý thất bại, vui lòng thử lại</span>
                            </div>
                        </div>
                    </div>

                    {/* 5. Dashboard & Hồ sơ */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">⚡</div>
                        <h3>Tính năng khác</h3>
                        <div className="guide-features">
                            <div className="guide-feature-item">
                                <strong>📈 Tổng quan</strong>
                                <span>Xem thống kê số lượng bài báo và tỷ lệ thành công của bạn.</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>👤 Hồ sơ tài khoản</strong>
                                <span>Chỉnh sửa tên hiển thị và cập nhật mật khẩu bảo mật.</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* === NỘI DUNG CHO ADMIN / ROOT === */}
            {activeTab === 'admin' && showAdminTab && (
                <div className="guide-content">
                    {/* 1. Tổng quan quyền */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">🔐</div>
                        <h3>Phân quyền</h3>
                        <div className="guide-role-table">
                            <div className="guide-role-row guide-role-header">
                                <span>Quyền hạn</span>
                                <span>👤 User</span>
                                <span>🛡️ Admin</span>
                                <span>👑 Root</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Tạo & xem tóm tắt</span>
                                <span>✅</span>
                                <span>✅</span>
                                <span>✅</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Truy cập quản trị</span>
                                <span>❌</span>
                                <span>✅</span>
                                <span>✅</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Quản lý người dùng</span>
                                <span>❌</span>
                                <span>✅</span>
                                <span>✅</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Đổi cấp độ tài khoản</span>
                                <span>❌</span>
                                <span>✅</span>
                                <span>✅</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Xóa tài khoản</span>
                                <span>❌</span>
                                <span>❌</span>
                                <span>✅</span>
                            </div>
                        </div>
                    </div>

                    {/* 2. Trang quản trị */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">⚙️</div>
                        <h3>Trang Quản trị hệ thống</h3>
                        <p>Truy cập qua menu góc trái dưới → <strong>⚙️ Quản trị hệ thống</strong></p>
                        <ol className="guide-steps">
                            <li><strong>Bảng thống kê:</strong> Theo dõi tổng quan dữ liệu toàn hệ thống.</li>
                            <li><strong>Dashboard Metabase:</strong> Phân tích dữ liệu chuyên sâu (nếu có).</li>
                            <li><strong>Danh sách tài khoản:</strong> Xem và quản lý tất cả người dùng.</li>
                        </ol>
                    </div>

                    {/* 3. Quản lý người dùng */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">👥</div>
                        <h3>Quản lý người dùng</h3>
                        <div className="guide-features">
                            <div className="guide-feature-item">
                                <strong>🔄 Trạng thái (Bật/Tắt)</strong>
                                <span>Khóa hoặc mở khóa tài khoản của người dùng.</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>🏷️ Đổi vai trò</strong>
                                <span>Admin / Root có thể nâng hoặc hạ quyền của người dùng (User ↔ Admin).</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>🗑️ Xóa tài khoản (Chỉ Root)</strong>
                                <span>Xóa vĩnh viễn dữ liệu. Hành động này không thể hoàn tác.</span>
                            </div>
                        </div>
                        <div className="guide-warning">
                            ⚠️ Bạn không thể tự khóa/xóa tài khoản của chính mình. Tài khoản cấp Root không thể bị xóa.
                        </div>
                    </div>

                    {/* 4. Giám sát hệ thống */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">📊</div>
                        <h3>Giám sát & Sự cố</h3>
                        <div className="guide-features">
                            <div className="guide-feature-item">
                                <strong>📈 Theo dõi Dashboard</strong>
                                <span>Kiểm tra tỷ lệ thành công. Tỷ lệ thấp thường do file bị hỏng hoặc lỗi AI.</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>🔴 Kiểm tra bài báo lỗi</strong>
                                <span>Bài báo báo lỗi sẽ có mô tả nguyên nhân để hỗ trợ khắc phục.</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>🔧 System Logs</strong>
                                <span>Quản trị viên cần kiểm tra Logs trên Render Dashboard để xem chi tiết lỗi kỹ thuật.</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default UserGuide;
