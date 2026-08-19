import {useState, useEffect } from 'react';
import api from '../api';
import { filterByTimeRange } from '../utils/timeFilter'

function Reviews ({ companyId, companyName }) {
    const [allReviews, setAllReviews] = useState([]);
    const [filteredReviews, setFilteredReviews] = useState([]);
    const [timeRange, setTimeRange] = useState('all');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (companyId) {
            api.get(`/companies/${companyId}/reviews`)
            .then((response) => {
                setAllReviews(response.data.reviews);
                setFilteredReviews(response.data.reviews);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching reviews:', error);
                setLoading(false);
            });
        }
    }, [companyId]);

    useEffect(() => {
        setFilteredReviews(filterByTimeRange(allReviews, timeRange, 'created_at'))
    }, [timeRange, allReviews])

    if (!companyId) return <div className="loading">Please select a company to view reviews.</div>

    if (loading) return <div className="loading">Loading company reviews...</div>

    return (
        <div>
            <div className="section-header">
                <h2 className="section-title">{companyName} has ({filteredReviews.length}) Reviews</h2>
                <select className="compare-select"
                onChange={(e) => setTimeRange(e.target.value)}
                style={{marginBottom:'16px'}}>
                    <option value="all">All Time</option>
                    <option value="6months">Last 6 Months</option>
                    <option value="1year">Last Year</option>
                    <option value="3year">Last 3 Years</option>
                </select>
            </div>
            {filteredReviews.map((review) => (
                <div key={review.id} className="review-item">
                    <div className="rating">
                        {'★'.repeat(review.rating || 0)}{'☆'.repeat(5 - (review.rating || 0))}
                        {review.rating ? ` ${review.rating}/5` : ' No rating'}
                    </div>
                    <div className="title">{review.content}</div>
                </div>
            ))}
        </div>
    )
}

export default Reviews;
