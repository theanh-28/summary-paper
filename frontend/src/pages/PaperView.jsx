import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';

function PaperView() {
    const { id } = useParams();
    const [paper, setPaper] = useState(null);
    const [summaries, setSummaries] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (id) {
            fetchData();
        }
    }, [id]);

    const fetchData = async () => {
        setLoading(true);
        try {
            // Lấy thông tin bài báo (để hiển thị title) 
            // Nếu API không có get paper by id thì mình cần API đó.
            // Nhưng hiện tại API back-end chưa chắc có /papers/:id, 
            // ta có thể fetch summaries trước và nếu cần thì dựa vào đó.
            // Để chắc chắn, ta sẽ gọi API summaries.
            const sumRes = await api.get(`/summaries/by-paper/${id}`);
            setSummaries(sumRes.data);
            
            // Lấy lại danh sách papers để tìm title (hoặc gọi API /papers/{id} nếu có)
            const papersRes = await api.get('/papers/');
            const foundPaper = papersRes.data.find(p => p.id === parseInt(id));
            if (foundPaper) setPaper(foundPaper);
            
        } catch (err) {
            console.error("Error fetching data", err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div style={{textAlign: 'center', marginTop: '5rem'}}>Đang tải dữ liệu...</div>;

    if (!paper && summaries.length === 0) {
        return <div style={{textAlign: 'center', marginTop: '5rem'}}>Không tìm thấy bài báo.</div>;
    }

    return (
        <div className="history-container" style={{maxWidth: '1000px', margin: '0 auto', padding: '2rem'}}>
            <div className="summaries-view glass-card" style={{padding: '3rem'}}>
                <h3 style={{marginBottom: '2rem', fontSize: '1.5rem'}}>
                    Kết quả AI cho: <span style={{color: 'var(--primary)'}}>{paper ? paper.title : `Bài báo #${id}`}</span>
                </h3>
                {summaries.length > 0 ? (
                    summaries.map(s => (
                        <div key={s.id} className="summary-card" style={{marginBottom: '2rem'}}>
                            <span className="badge" style={{marginBottom: '1rem', display: 'inline-block'}}>{s.type}</span>
                            <p style={{lineHeight: '1.8', fontSize: '1.05rem', whiteSpace: 'pre-wrap'}}>{s.content}</p>
                            <div style={{marginTop: '1rem', color: 'var(--text-muted)', fontSize: '0.9rem'}}>
                                Tạo lúc: {new Date(s.created_at).toLocaleString('vi-VN')}
                            </div>
                        </div>
                    ))
                ) : (
                    <p style={{color: 'var(--text-muted)'}}>Chưa có bản tóm tắt nào cho bài báo này.</p>
                )}
            </div>
        </div>
    );
}

export default PaperView;
