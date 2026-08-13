import React, { useState } from 'react';
import Companies from './components/CompanyList';
import Reviews from './components/ReviewFeed';
import Insights from './components/InsightsPanel';
import Compare from './components/ComparisonView';
import './App.css';

const App = () => {
  console.log('Wohoo, App rendered');
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [view, setView] = useState('companies');

  const handleCompanySelect = (company) => {
    setSelectedCompany(company);
    setView('reviews');
  };

  const renderView = () => {
    switch (view) {
      case 'companies':
        return <Companies onCompanySelect={handleCompanySelect} />;
      case 'reviews':
        return <Reviews companyId={selectedCompany?.id} companyName={selectedCompany?.name} />;
      case 'insights':
        return <Insights companyId={selectedCompany?.id} companyName={selectedCompany?.name} />;
      case 'compare':
        return <Compare companyAId={selectedCompany?.id} companyAName={selectedCompany?.name} />;
      default:
        return <Companies onCompanySelect={handleCompanySelect} />;
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1><span>Trust</span>Lens</h1>
        <p style={{ color: '#8899AA', fontSize: '0.9rem', marginTop: '4px' }}>
          Employer Review Intelligence Dashboard
        </p>
      </header>

      <nav className="nav-bar">
        <button
          className={`nav-btn ${view === 'companies' ? 'active' : ''}`}
          onClick={() => setView('companies')}>
          Companies
        </button>
        <button
          className={`nav-btn ${view === 'reviews' ? 'active' : ''}`}
          onClick={() => setView('reviews')}>
          Reviews
        </button>
        <button
          className={`nav-btn ${view === 'insights' ? 'active' : ''}`}
          onClick={() => setView('insights')}>
          Insights
        </button>
        <button
          className={`nav-btn ${view === 'compare' ? 'active' : ''}`}
          onClick={() => setView('compare')}>
          Compare
        </button>
      </nav>

      {renderView()}

    </div>
  )
};


export default App;