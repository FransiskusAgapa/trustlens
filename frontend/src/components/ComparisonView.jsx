import {useState, useEffect } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'
const COLORS = ['#0D7377', '#C0392B', '#F4A261'];

function getSentimentData(insights) {
    const count = {positive: 0, negative: 0, neutral: 0}
    insights.forEach(insight => {
            const label = insight.sentiment_label.toLowerCase()
            if (count[label] != undefined) count[label]++
        }
    )

    return [
        {name: 'Positive', value: count.positive},
        {name: 'Negative', value: count.negative},
        {name: 'Neutral', value: count.neutral}
    ]
}

function getDepartmentSummary(insights) {
    const departmentSummary = {}

    insights.forEach(insight => {
        const department = insight.department_tag
        if (!departmentSummary[department]) {
            departmentSummary[department] = {
                total: 0,
                positive: 0,
                negative: 0,
                neutral: 0,
            }
        }
        departmentSummary[department].total++
        const label = insight.sentiment_label.toLowerCase()
        if (departmentSummary[department][label] != undefined) departmentSummary[department][label]++
    })

    return Object.entries(departmentSummary)
        .map(([department, data]) => {
            const dominantSentiment = ['positive', 'negative', 'neutral'].reduce((a, b) => data[a] > data[b] ? a : b)
            return {
                department,
                total: data.total,
                positive: data.positive,
                negative: data.negative,
                neutral: data.neutral,
                dominantSentiment
            }
        })
        .sort((a, b) => b.total - a.total)
}

function Compare({ companyAId, companyAName }) {
    const [selectedCompanyBId, setSelectedCompanyBId] = useState(null);
    const [selectedCompanyBName, setSelectedCompanyBName] = useState(null);

    const [companies, setCompanies] = useState([])

    const [insightA, setInsightA] = useState([])
    const [insightB, setInsightB] = useState([])

    useEffect(() => {
        axios.get(`https://trustlens-api-bywi.onrender.com/companies`)
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
            axios.get(`https://trustlens-api-bywi.onrender.com/companies/${companyAId}/insights`)
            .then((response) => {
                setInsightA(response.data.insights)
            })
            .catch((error) => {
                console.error('Error fetching insight for company A:', error);
            });
        }
        if (selectedCompanyBId) {
            axios.get(`https://trustlens-api-bywi.onrender.com/companies/${selectedCompanyBId}/insights`)
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
            <div className="compare-selector">
                <label className="section-title">Compare against:&nbsp;&nbsp;&nbsp;</label>
                <select
                    className="compare-select"
                    onChange={(e) => setSelectedCompanyBId(e.target.value)}>
                    <option value="">Select a company</option>
                    {companies.map(company => (
                        <option key={company.id} value={company.id}>{company.name}</option>
                    ))}
                </select>
            </div>

            <div className="comparison-grid">
                <div className="comparison-card">
                    <h3>{companyAName || 'Company A'}</h3>
                    <p style={{color: '#8899AA', fontSize: '0.8rem', marginBottom: '8px'}}>
                        Based on {insightA.length} reviews
                        {insightA.length > 0 && ` (${new Date(insightA[insightA.length-1].review_date).getFullYear()} - ${new Date(insightA[0].review_date).getFullYear()})`}
                    </p>
                    <div>
                        <PieChart width={250} height={280}>
                            <Pie
                                data={getSentimentData(insightA)}
                                cx={125}
                                cy={110}
                                outerRadius={80}
                                dataKey="value"
                                label={false}>
                                {getSentimentData(insightA).map((entry, index) => (
                                    <Cell key={index} fill={COLORS[index]} />
                                ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                        </PieChart>
                        <div className="dept-list">
                            {getDepartmentSummary(insightA).slice(0, 3).map((dept, i) => (
                                <div key={i} className="dept-item">
                                    <span className={`dept-dot dept-dot-${dept.dominantSentiment}`}></span>
                                    <span className="dept-name">{dept.department}</span>
                                    <span className="dept-count">{dept.total} mentions</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                    <div className="comparison-card">
                        <h3>{companies.find(c => c.id == selectedCompanyBId)?.name || 'Select a company'}</h3>
                        <p style={{color: '#8899AA', fontSize: '0.8rem', marginBottom: '8px'}}>
                            Based on {insightB.length} reviews
                            {insightB.length > 0 && ` (${new Date(insightB[insightB.length-1].review_date).getFullYear()} - ${new Date(insightB[0].review_date).getFullYear()})`}
                        </p>
                        {selectedCompanyBId && insightB.length > 0 ? (
                            <div>
                                <PieChart width={250} height={280}>
                                    <Pie
                                        data={getSentimentData(insightB)}
                                        cx={125}
                                        cy={110}
                                        outerRadius={80}
                                        dataKey="value"
                                        label={false}>
                                        {getSentimentData(insightB).map((entry, index) => (
                                            <Cell key={index} fill={COLORS[index]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                    <Legend />
                                </PieChart>
                                <div className="dept-list">
                                    {getDepartmentSummary(insightB).slice(0, 3).map((dept, i) => (
                                        <div key={i} className="dept-item">
                                            <span className={`dept-dot dept-dot-${dept.dominantSentiment}`}></span>
                                            <span className="dept-name">{dept.department}</span>
                                            <span className="dept-count">{dept.total} mentions</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                        <div className="loading">Select a company to compare</div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Compare;