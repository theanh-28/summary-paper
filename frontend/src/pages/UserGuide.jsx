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
                            <strong>AI Summary</strong> là công cụ tóm tắt bài báo khoa học tự động bằng AI.
                            Bạn chỉ cần upload file, hệ thống sẽ trích xuất nội dung và tạo bản tóm tắt ngắn gọn bằng tiếng Việt.
                        </p>
                        <div className="guide-highlight">
                            💡 Hỗ trợ file: <strong>PDF</strong>, <strong>DOCX</strong> và <strong>TXT</strong>
                        </div>
                    </div>

                    {/* 2. Upload & Tóm tắt */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">📤</div>
                        <h3>Bước 1 — Upload bài báo</h3>
                        <ol className="guide-steps">
                            <li>Nhấn <strong>✍️ Tạo Tóm Tắt</strong> ở sidebar bên trái</li>
                            <li>Nhập <strong>tiêu đề</strong> cho bài báo</li>
                            <li>Chọn file từ máy tính (PDF, DOCX hoặc TXT)</li>
                            <li>Nhấn <strong>Tải lên & Tóm tắt</strong></li>
                        </ol>
                        <div className="guide-note">
                            ⏳ Quá trình xử lý mất khoảng <strong>30 giây – 3 phút</strong> tùy độ dài bài báo.
                            Bạn có thể rời trang, hệ thống vẫn xử lý ở nền.
                        </div>
                    </div>

                    {/* 3. Xem kết quả */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">📋</div>
                        <h3>Bước 2 — Xem kết quả tóm tắt</h3>
                        <ol className="guide-steps">
                            <li>Sau khi xử lý xong, trạng thái chuyển thành <span className="status-pill status-completed">✅ Hoàn tất</span></li>
                            <li>Nhấn vào bài báo ở mục <strong>"Gần đây"</strong> trên sidebar để xem chi tiết</li>
                            <li>Nội dung tóm tắt hiển thị bên dưới thông tin bài báo</li>
                        </ol>
                    </div>

                    {/* 4. Trạng thái bài báo */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">🔄</div>
                        <h3>Các trạng thái bài báo</h3>
                        <div className="guide-status-grid">
                            <div className="guide-status-item">
                                <span className="status-pill status-uploaded">📄 Đã tải</span>
                                <span>File đã upload, chờ xử lý</span>
                            </div>
                            <div className="guide-status-item">
                                <span className="status-pill status-processing">⏳ Đang xử lý</span>
                                <span>AI đang trích xuất và tóm tắt</span>
                            </div>
                            <div className="guide-status-item">
                                <span className="status-pill status-completed">✅ Hoàn tất</span>
                                <span>Tóm tắt đã sẵn sàng</span>
                            </div>
                            <div className="guide-status-item">
                                <span className="status-pill status-failed">❌ Lỗi</span>
                                <span>Xử lý thất bại — thử upload lại</span>
                            </div>
                        </div>
                    </div>

                    {/* 5. Dashboard & Hồ sơ */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">⚡</div>
                        <h3>Các tính năng khác</h3>
                        <div className="guide-features">
                            <div className="guide-feature-item">
                                <strong>📈 Dashboard</strong>
                                <span>Xem thống kê số bài đã xử lý, tỷ lệ thành công</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>👤 Hồ sơ tài khoản</strong>
                                <span>Cập nhật tên hiển thị, đổi mật khẩu</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>📂 Lịch sử</strong>
                                <span>Xem lại tất cả bài báo đã upload ở sidebar "Gần đây"</span>
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
                        <h3>Phân quyền hệ thống</h3>
                        <div className="guide-role-table">
                            <div className="guide-role-row guide-role-header">
                                <span>Quyền hạn</span>
                                <span>👤 User</span>
                                <span>🛡️ Admin</span>
                                <span>👑 Root</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Upload & xem tóm tắt</span>
                                <span>✅</span>
                                <span>✅</span>
                                <span>✅</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Dashboard cá nhân</span>
                                <span>✅</span>
                                <span>✅</span>
                                <span>✅</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Quản trị hệ thống</span>
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
                                <span>Xóa / vô hiệu hóa tài khoản</span>
                                <span>❌</span>
                                <span>⚠️ Hạn chế</span>
                                <span>✅</span>
                            </div>
                            <div className="guide-role-row">
                                <span>Thay đổi vai trò người dùng</span>
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
                        <p>Truy cập qua menu tài khoản → <strong>⚙️ Quản trị hệ thống</strong></p>
                        <ol className="guide-steps">
                            <li><strong>Bảng thống kê:</strong> Tổng số người dùng, bài báo, tóm tắt và tỷ lệ xử lý thành công</li>
                            <li><strong>Bảng Metabase:</strong> Dashboard phân tích dữ liệu nâng cao (nếu đã cấu hình)</li>
                            <li><strong>Danh sách người dùng:</strong> Xem, kích hoạt/vô hiệu hóa và quản lý tài khoản</li>
                        </ol>
                    </div>

                    {/* 3. Quản lý người dùng */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">👥</div>
                        <h3>Quản lý người dùng</h3>
                        <div className="guide-features">
                            <div className="guide-feature-item">
                                <strong>🔄 Kích hoạt / Vô hiệu hóa</strong>
                                <span>Nhấn nút bật/tắt ở cột "Trạng thái" để kích hoạt hoặc khóa tài khoản</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>🗑️ Xóa tài khoản</strong>
                                <span>Chỉ Root mới có thể xóa tài khoản. Thao tác này không thể hoàn tác</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>🏷️ Đổi vai trò</strong>
                                <span>Chỉ Root mới có thể nâng/hạ quyền người dùng (user ↔ admin)</span>
                            </div>
                        </div>
                        <div className="guide-warning">
                            ⚠️ <strong>Lưu ý:</strong> Không thể tự vô hiệu hóa hoặc xóa chính tài khoản của mình.
                            Tài khoản Root không thể bị xóa bởi bất kỳ ai.
                        </div>
                    </div>

                    {/* 4. Giám sát hệ thống */}
                    <div className="glass-card guide-section">
                        <div className="guide-section-icon">📊</div>
                        <h3>Giám sát & Xử lý sự cố</h3>
                        <div className="guide-features">
                            <div className="guide-feature-item">
                                <strong>📈 Theo dõi Dashboard</strong>
                                <span>Kiểm tra tỷ lệ xử lý thành công. Nếu tỷ lệ thấp, có thể do lỗi kết nối AI hoặc file không hợp lệ</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>🔴 Bài báo lỗi</strong>
                                <span>Bài có trạng thái "failed" sẽ hiển thị lý do lỗi. Người dùng có thể thử upload lại</span>
                            </div>
                            <div className="guide-feature-item">
                                <strong>🔧 Kiểm tra Render Logs</strong>
                                <span>Truy cập Render Dashboard → Service → Logs để xem chi tiết lỗi backend</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default UserGuide;
