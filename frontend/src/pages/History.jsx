import { useState, useEffect } from 'react';
import api from '../services/api';

function History() {
    const [papers, setPapers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedPaper, setSelectedPaper] = useState(null);
    const [summaries, setSummaries] = useState([]);

    useEffect(() => {
        fetchPapers();
    }, []);

    const fetchPapers = async () => {
        try {
            const res = await api.get('/papers/');
            setPapers(res.data);
        } catch (err) {
            console.error("Error fetching papers", err);
        } finally {
            setLoading(false);
        }
    };

    const viewSummaries = async (paper) => {
        setSelectedPaper(paper);
        try {
            const res = await api.get(`/summaries/by-paper/${paper.id}`);
            setSummaries(res.data);
        } catch (err) {
            console.error("Error fetching summaries", err);
        }
    };

    if (loading) return <div style={{textAlign: 'center', marginTop: '5rem'}}>Loading history...</div>;

    return (
        <div className="history-container">
            <h2 style={{marginBottom: '2rem'}}>Lịch sử của bạn</h2>
            <div className="history-layout">
                <div className="papers-list glass-card">
                    <h3 style={{marginBottom: '1.5rem'}}>Bài báo đã tải lên</h3>
                    {papers.map(p => (
                        <div key={p.id} className="paper-card" onClick={() => viewSummaries(p)}>
                            <h4 style={{marginBottom: '0.5rem'}}>{p.title}</h4>
                            <small style={{color: 'var(--text-muted)'}}>
                                {new Date(p.created_at).toLocaleDateString()}
                            </small>
                        </div>
                    ))}
                    {papers.length === 0 && <p style={{color: 'var(--text-muted)'}}>Bạn chưa tải lên bài báo nào.</p>}
                </div>

                <div className="summaries-view glass-card">
                    {selectedPaper ? (
                        <>
                            <h3 style={{marginBottom: '1.5rem'}}>Tóm tắt cho: <span style={{color: 'var(--primary)'}}>{selectedPaper.title}</span></h3>
                            {summaries.length > 0 ? (
                                summaries.map(s => (
                                    <div key={s.id} className="summary-card">
                                        <span className="badge">{s.type}</span>
                                        <p style={{lineHeight: '1.6', marginBottom: '1rem'}}>{s.content}</p>
                                        <small style={{color: 'var(--text-muted)'}}>
                                            Tạo lúc: {new Date(s.created_at).toLocaleString()}
                                        </small>
                                    </div>
                                ))
                            ) : (
                                <p style={{color: 'var(--text-muted)'}}>Chưa có bản tóm tắt nào cho bài báo này.</p>
                            )}
                        </>
                    ) : (
                        <div style={{display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center'}}>
                            <p style={{color: 'var(--text-muted)', fontSize: '1.1rem'}}>Chọn một bài báo bên trái để xem kết quả AI.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default History;
