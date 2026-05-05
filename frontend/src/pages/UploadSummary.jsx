import { useState } from 'react';
import api from '../services/api';

function UploadSummary() {
    const [file, setFile] = useState(null);
    const [title, setTitle] = useState('');
    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState(null);
    const [error, setError] = useState('');

    const handleUploadAndSummarize = async (e) => {
        e.preventDefault();
        if (!file || !title) return;

        setLoading(true);
        setError('');
        setSummary(null);

        try {
            // 1. Upload file
            const formData = new FormData();
            formData.append('file', file);
            formData.append('title', title);

            const uploadRes = await api.post('/papers/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const paperId = uploadRes.data.id;

            // 2. Generate summary
            const summaryRes = await api.post('/summaries/generate', {
                paper_id: paperId,
                type: 'short'
            });

            setSummary(summaryRes.data);
        } catch (err) {
            console.error(err);
            setError('Có lỗi xảy ra khi xử lý file. Vui lòng thử lại.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <div className="glass-card" style={{maxWidth: '600px', margin: '0 auto'}}>
                <h2 style={{marginBottom: '1rem'}}>Upload & Summarize</h2>
                <p style={{marginBottom: '2rem', color: 'var(--text-muted)'}}>Tải lên file PDF để hệ thống AI tự động phân tích và tóm tắt</p>
                
                <form onSubmit={handleUploadAndSummarize}>
                    <input 
                        type="text" 
                        placeholder="Tiêu đề bài báo..." 
                        value={title} 
                        onChange={e => setTitle(e.target.value)} 
                        required 
                    />
                    <input 
                        type="file" 
                        accept=".pdf" 
                        onChange={e => setFile(e.target.files[0])} 
                        required 
                        style={{padding: '0.8rem'}}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? 'Đang phân tích bằng AI...' : 'Tạo Tóm Tắt'}
                    </button>
                </form>

                {error && <p className="error" style={{marginTop: '1rem'}}>{error}</p>}
                
                {summary && (
                    <div className="summary-card" style={{marginTop: '2rem'}}>
                        <h3 style={{marginBottom: '1rem'}}>Kết quả Tóm tắt:</h3>
                        <span className="badge">{summary.type}</span>
                        <p style={{lineHeight: '1.6'}}>{summary.content}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default UploadSummary;
