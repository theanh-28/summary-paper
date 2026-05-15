import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function UploadSummary() {
    const [file, setFile] = useState(null);
    const [title, setTitle] = useState('');
    const [uploading, setUploading] = useState(false);
    const [processing, setProcessing] = useState(false);
    const [paperStatus, setPaperStatus] = useState(null); // uploaded | processing | completed | failed
    const [paperId, setPaperId] = useState(null);
    const [summary, setSummary] = useState(null);
    const [error, setError] = useState('');
    const [progress, setProgress] = useState(0);
    const pollingRef = useRef(null);
    const navigate = useNavigate();

    // Cleanup polling on unmount
    useEffect(() => {
        return () => {
            if (pollingRef.current) {
                clearInterval(pollingRef.current);
            }
        };
    }, []);

    const startPolling = (id) => {
        // Polling mỗi 3 giây để kiểm tra trạng thái
        pollingRef.current = setInterval(async () => {
            try {
                const res = await api.get(`/papers/${id}`);
                const status = res.data.status;
                setPaperStatus(status);

                if (status === 'processing') {
                    // Fake progress animation
                    setProgress(prev => Math.min(prev + Math.random() * 15, 90));
                }

                if (status === 'completed') {
                    clearInterval(pollingRef.current);
                    setProcessing(false);
                    setProgress(100);
                    
                    // Fetch summary
                    try {
                        const sumRes = await api.get(`/summaries/by-paper/${id}`);
                        if (sumRes.data.length > 0) {
                            setSummary(sumRes.data[sumRes.data.length - 1]); // Lấy summary mới nhất
                        }
                    } catch (err) {
                        console.error('Error fetching summary:', err);
                    }
                }

                if (status === 'failed') {
                    clearInterval(pollingRef.current);
                    setProcessing(false);
                    setProgress(0);
                    setError(res.data.error_message || 'Xử lý thất bại. Vui lòng thử lại.');
                }
            } catch (err) {
                console.error('Polling error:', err);
            }
        }, 3000);
    };

    const handleUploadAndSummarize = async (e) => {
        e.preventDefault();
        if (!file || !title) return;

        setUploading(true);
        setError('');
        setSummary(null);
        setPaperStatus(null);
        setProgress(0);

        try {
            // 1. Upload file → nhận 202 Accepted ngay lập tức
            const formData = new FormData();
            formData.append('file', file);
            formData.append('title', title);

            const uploadRes = await api.post('/papers/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const id = uploadRes.data.id;
            setPaperId(id);
            setPaperStatus('uploaded');
            setUploading(false);
            setProcessing(true);
            setProgress(10);

            // 2. Bắt đầu polling để theo dõi trạng thái
            startPolling(id);

        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Có lỗi xảy ra khi upload file. Vui lòng thử lại.');
            setUploading(false);
        }
    };

    const getStatusMessage = () => {
        switch (paperStatus) {
            case 'uploaded': return '📤 File đã upload thành công. Đang chờ xử lý...';
            case 'processing': return '🤖 AI đang phân tích và tóm tắt nội dung...';
            case 'completed': return '✅ Hoàn tất! Xem kết quả bên dưới.';
            case 'failed': return '❌ Xử lý thất bại.';
            default: return '';
        }
    };

    const getStatusClass = () => {
        switch (paperStatus) {
            case 'completed': return 'status-completed';
            case 'failed': return 'status-failed';
            case 'processing': return 'status-processing';
            default: return 'status-pending';
        }
    };

    return (
        <div className="upload-container">
            <div className="glass-card upload-card">
                <div className="upload-header">
                    <h2>Upload & Summarize</h2>
                    <p>Tải lên file PDF, TXT hoặc DOCX để hệ thống AI tự động phân tích và tóm tắt</p>
                </div>
                
                <form onSubmit={handleUploadAndSummarize} className="upload-form">
                    <div className="form-group">
                        <label htmlFor="paper-title">Tiêu đề bài báo</label>
                        <input 
                            id="paper-title"
                            type="text" 
                            placeholder="Nhập tiêu đề bài báo..." 
                            value={title} 
                            onChange={e => setTitle(e.target.value)} 
                            required 
                            disabled={uploading || processing}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="paper-file">Chọn file</label>
                        <div className="file-input-wrapper">
                            <input 
                                id="paper-file"
                                type="file" 
                                accept=".pdf,.txt,.docx" 
                                onChange={e => setFile(e.target.files[0])} 
                                required 
                                disabled={uploading || processing}
                            />
                            {file && (
                                <div className="file-info">
                                    📎 {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                                </div>
                            )}
                        </div>
                    </div>

                    <button type="submit" disabled={uploading || processing}>
                        {uploading ? '⏳ Đang upload...' : processing ? '🤖 Đang xử lý...' : '🚀 Tạo Tóm Tắt'}
                    </button>
                </form>

                {/* Processing Status */}
                {paperStatus && (
                    <div className={`processing-status ${getStatusClass()}`}>
                        <div className="status-message">{getStatusMessage()}</div>
                        {(paperStatus === 'processing' || paperStatus === 'uploaded') && (
                            <div className="progress-bar-container">
                                <div 
                                    className="progress-bar" 
                                    style={{ width: `${progress}%` }}
                                />
                                <span className="progress-text">{Math.round(progress)}%</span>
                            </div>
                        )}
                    </div>
                )}

                {error && <p className="error">{error}</p>}
                
                {/* Summary Result */}
                {summary && (
                    <div className="summary-result">
                        <div className="summary-card">
                            <div className="summary-header">
                                <h3>📝 Kết quả Tóm tắt</h3>
                                {paperId && (
                                    <button 
                                        className="btn-view-detail"
                                        onClick={() => navigate(`/paper/${paperId}`)}
                                    >
                                        Xem chi tiết →
                                    </button>
                                )}
                            </div>
                            <p className="summary-content">{summary.content}</p>
                            <div className="summary-meta">
                                Tạo lúc: {new Date(summary.created_at).toLocaleString('vi-VN')}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default UploadSummary;
