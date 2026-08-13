import { useState, useEffect } from 'react';
import axios from 'axios';

function Companies({ onCompanySelect }) {
    const [companies, setCompanies] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('https://trustlens-api-bywi.onrender.com/companies')
            .then((response) => {
                setCompanies(response.data.companies);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching companies:', error);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="loading">Loading companies...</div>

    return (
        <div>
            <h2 className="section-title">Companies ({companies.length})</h2>
            {companies.map(company => (
                <div
                    key={company.id}
                    className="card"
                    onClick={() => onCompanySelect(company)}>
                    <h3>{company.name}</h3>
                    <p>{company.industry}</p>
                </div>
            ))}
        </div>
    );
}

export default Companies;