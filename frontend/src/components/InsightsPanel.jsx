import {useState, useEffect } from 'react';
import axios from 'axios';

function Insights({ companyId, companyName }) {
    const [allInsights, setAllInsights] = useState([]);
    const [filteredInsights, setFilteredInsights] = useState([]);
    const [timeRange, setTimeRange] = useState('all');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (companyId) {
            axios.get(`https://trustlens-api-bywi.onrender.com/companies/${companyId}/insights`)
            .then((response) => {
                setAllInsights(response.data.insights);
                setFilteredInsights(response.data.insights);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching insights:', error);
                setLoading(false);
            });
        }
    }, [companyId]);

    useEffect( () => {
        if (timeRange === 'all') {
            setFilteredInsights(allInsights);
            return;
        }

        const months = timeRange === '6months' ? 6 : timeRange === "1year" ? 12 : 36
        const cutoff = new Date();
        cutoff.setMonth(cutoff.getMonth() - months);
        setFilteredInsights(allInsights.filter(insight => new Date(insight.review_date) >= cutoff));
    }, [timeRange, allInsights]);

    if (!companyId) return <div className="loading">Please select a company to view insights.</div>

    if (loading) return <div className="loading">Loading company insights...</div>

    return (
        <div>
            <div className="section-header">
                <h2 className="section-title">{companyName} has ({filteredInsights.length}) Insights</h2>
                <select className="compare-select"
                onChange={(e) => setTimeRange(e.target.value)}
                style={{marginBottom:'16px'}}>
                    <option value="all">All Time</option>
                    <option value="6months">Last 6 Months</option>
                    <option value="1year">Last Year</option>
                    <option value="3years">Last 3 Years</option>
                </select>
            </div>

            {filteredInsights.map((insight, index) => (
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

