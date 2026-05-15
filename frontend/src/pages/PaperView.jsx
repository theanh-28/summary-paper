import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';

function PaperView() {
    const { id } = useParams();
    const [paper, setPaper] = useState(null);
    const [summaries, setSummaries] = useState([]);
    const [loading, setLoading] = useState(true);
    const pollingRef = useRef(null);

    useEffect(() => {
        if (id) {
            fetchData();
        }
        return () => {
            if (pollingRef.current) {
                clearInterval(pollingRef.current);
            }
        };
    }, [id]);

    const fetchData = async () => {
        setLoading(true);
        try {
            // Lấy thông tin paper trực tiếp
            const paperRes = await api.get(`/papers/${id}`);
            setPaper(paperRes.data);

            if (paperRes.data.status === 'completed') {
                // Lấy summaries nếu đã completed
                const sumRes = await api.get(`/summaries/by-paper/${id}`);
                setSummaries(sumRes.data);
            } else if (paperRes.data.status === 'processing' || paperRes.data.status === 'uploaded') {
                // Bắt đầu polling nếu đang xử lý
                startPolling();
            }
        } catch (err) {
            console.error("Error fetching data", err);
        } finally {
            setLoading(false);
        }
    };

    const startPolling = () => {
        if (pollingRef.current) clearInterval(pollingRef.current);
        
        pollingRef.current = setInterval(async () => {
            try {
                const res = await api.get(`/papers/${id}`);
                setPaper(res.data);

                if (res.data.status === 'completed') {
                    clearInterval(pollingRef.current);
                    const sumRes = await api.get(`/summaries/by-paper/${id}`);
                    setSummaries(sumRes.data);
                }

                if (res.data.status === 'failed') {
                    clearInterval(pollingRef.current);
                }
            } catch (err) {
                console.error("Polling error:", err);
            }
        }, 3000);
    };

    const handleRegenerate = async () => {
        try {
            await api.post('/summaries/generate', { paper_id: parseInt(id) });
            setPaper(prev => ({ ...prev, status: 'uploaded' }));
            startPolling();
        } catch (err) {
            console.error("Error regenerating:", err);
        }
    };

    if (loading) {
        return (
            <div className="paper-view-loading">
                <div className="spinner"></div>
                <p>Đang tải dữ liệu...</p>
            </div>
        );
    }

    if (!paper) {
        return (
            <div className="paper-view-empty">
                <p>Không tìm thấy bài báo.</p>
            </div>
        );
    }

    return (
        <div className="paper-view-container">
            <div className="glass-card paper-detail-card">
                {/* Paper Header */}
                <div className="paper-detail-header">
                    <h2>{paper.title}</h2>
                    <div className="paper-meta-row">
                        <span className={`status-pill status-${paper.status}`}>
                            {paper.status === 'uploaded' && '📤 Đã upload'}
                            {paper.status === 'processing' && '⏳ Đang xử lý'}
                            {paper.status === 'completed' && '✅ Hoàn tất'}
                            {paper.status === 'failed' && '❌ Thất bại'}
                        </span>
                        {paper.page_count && (
                            <span className="meta-tag">📄 {paper.page_count} trang</span>
                        )}
                        {paper.processing_time_seconds && (
                            <span className="meta-tag">⏱️ {paper.processing_time_seconds}s</span>
                        )}
                        <span className="meta-tag">
                            📅 {new Date(paper.created_at).toLocaleString('vi-VN')}
                        </span>
                    </div>
                </div>

                {/* Processing Status */}
                {(paper.status === 'processing' || paper.status === 'uploaded') && (
                    <div className="processing-indicator">
                        <div className="pulse-dot"></div>
                        <span>AI đang phân tích nội dung...</span>
                        <div className="processing-spinner"></div>
                    </div>
                )}

                {/* Error Message */}
                {paper.status === 'failed' && (
                    <div className="error-banner">
                        <p>❌ {paper.error_message || 'Xử lý thất bại.'}</p>
                        <button className="btn-retry" onClick={handleRegenerate}>
                            🔄 Thử lại
                        </button>
                    </div>
                )}

                {/* Summaries */}
                {paper.status === 'completed' && (
                    <div className="summaries-section">
                        <div className="section-header">
                            <h3>📝 Kết quả AI</h3>
                            <button className="btn-regenerate" onClick={handleRegenerate}>
                                🔄 Tạo lại
                            </button>
                        </div>
                        
                        {summaries.length > 0 ? (
                            summaries.map(s => (
                                <div key={s.id} className="summary-card">
                                    <p className="summary-text">{s.content}</p>
                                    <div className="summary-footer">
                                        Tạo lúc: {new Date(s.created_at).toLocaleString('vi-VN')}
                                    </div>
                                </div>
                            ))
                        ) : (
                            <p className="text-muted">Chưa có bản tóm tắt nào.</p>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default PaperView;
