import {useState, useEffect } from 'react';
import axios from 'axios';

function Compare({ companyAId, companyAName }) {
    const [selectedCompanyBId, setSelectedCompanyBId] = useState(null);
    const [selectedCompanyBName, setSelectedCompanyBName] = useState(null);

    const [companies, setCompanies] = useState([])

    const [insightA, setInsightA] = useState([])
    const [insightB, setInsightB] = useState([])

    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/companies`)
        .then((response) => {
            setCompanies(response.data.companies)
        })
        .catch((error) => {
            console.error('Error fetching companies:', error);
        }
    )
    }, [])

    useEffect(() => {
        if (companyAId) {
            axios.get(`http://127.0.0.1:8000/companies/${companyAId}/insights`)
            .then((response) => {
                setInsightA(response.data.insights)
            })
            .catch((error) => {
                console.error('Error fetching insight for company A:', error);
            });
        }
        if (selectedCompanyBId) {
            axios.get(`http://127.0.0.1:8000/companies/${selectedCompanyBId}/insights`)
            .then((response) => {
                setInsightB(response.data.insights)
            })
            .catch((error) => {
                console.error('Error fetching insight for company B:', error);
            });
        }
    }, [companyAId, selectedCompanyBId])


    return (
        <div>
            {/* <h2 className="section-title">Compare Companies</h2> */}
            <div style={{marginBottom: '24px'}}>
                <label className="section-title">Compare against:</label>
                <select 
                    onChange={(e) => setSelectedCompanyBId(e.target.value)}
                    style={{background: '#1B2A4A', color: '#E9ECEF', border: '1px solid #243558', padding: '8px', borderRadius: '6px'}}>
                    <option value="">Select a company</option>
                    {companies.map(company => (
                        <option key={company.id} value={company.id}>{company.name}</option>
                    ))}
                </select>
            </div>

            <div className="comparison-grid">
                <div className="comparison-card">
                    <h3>{companyAName || 'Company A'}</h3>
                    {insightA.map((insight, i) => (
                        <div key={i} style={{marginBottom: '8px'}}>
                            <span className={`badge badge-${insight.sentiment_label}`}>{insight.sentiment_label}</span>
                            <span style={{color: '#8899AA', fontSize: '0.85rem', marginLeft: '8px'}}>{insight.department_tag}</span>
                        </div>
                    ))}
                </div>

                <div className="comparison-card">
                    <h3>{selectedCompanyBId ? 'Company B' : 'Select a company'}</h3>
                    {insightB.map((insight, i) => (
                        <div key={i} style={{marginBottom: '8px'}}>
                            <span className={`badge badge-${insight.sentiment_label}`}>{insight.sentiment_label}</span>
                            <span style={{color: '#8899AA', fontSize: '0.85rem', marginLeft: '8px'}}>{insight.department_tag}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}




export default Compare;