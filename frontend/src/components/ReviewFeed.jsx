// placeholder for 'Reviews'

import {useState, useEffect } from 'react';
import axios from 'axios';

function Reviews ({ companyId, companyName }) {
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (companyId) {
            axios.get(`https://trustlens-api-bywi.onrender.com/companies/${companyId}/reviews`)
            .then((response) => {
                setReviews(response.data.reviews);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching reviews:', error);
                setLoading(false);
            });
        }
    }, [companyId]);

    if (!companyId) return <div className="loading">Please select a company to view reviews.</div>

    if (loading) return <div className="loading">Loading company reviews...</div>

    return (
        <div>
            <h2 className="section-title">{companyName} has ({reviews.length}) Reviews</h2>
            {reviews.map((review, index) => (
                <div key={index} className="review-item">
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

