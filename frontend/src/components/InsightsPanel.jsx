import {useState, useEffect } from 'react';
import axios from 'axios';

function Insights({ companyId, companyName }) {
    const [insights, setInsights] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (companyId) {
            axios.get(`https://trustlens-api-bywi.onrender.com/companies/${companyId}/insights`)
            .then((response) => {
                setInsights(response.data.insights);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching insights:', error);
                setLoading(false);
            });
        }
    }, [companyId]);

    if (!companyId) return <div className="loading">Please select a company to view insights.</div>

    if (loading) return <div className="loading">Loading company insights...</div>

    return (
        <div>
            <h2 className="section-title">Insights for {companyName}</h2>
            {insights.map((insight, index) => (
                <div key={index}>
                    <div key={index} className="review-item">
                        <div style={{display:'flex', alignItems:'center', gap:'10px', marginBottom:'8px'}}>
                            <span className={`badge badge-${insight.sentiment_label}`}>
                                {insight.sentiment_label}
                            </span>
                            <span style={{color:'#8899AA', fontSize:'0.85rem'}}>
                                {(insight.sentiment_score * 100).toFixed(0)}%
                            </span>
                            <span style={{color:'#F4A261', fontSize:'0.85rem'}}>
                                {insight.department_tag}
                            </span>
                        </div>
                        <p style={{color:'#8899AA', fontSize:'0.85rem', marginBottom:'8px'}}>{insight.summary}</p>
                        <div className="themes">
                            {insight.themes.map((theme, i) => (
                                <span key={i} className="theme-tag">{theme}</span>
                            ))}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Insights;

