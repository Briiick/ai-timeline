import './App.css';
import React from 'react';
import SummaryList from './components/SummaryList';

require('dotenv').config();

const App = () => {
  return (
    <div>
      <div className="header">
        <div className="header-content">
          <div className="header-left"><h1>AI Timeline</h1></div>
          <div className="header-right"><p><i>Start date: 03/04/2024. Current date: {new Date().toLocaleDateString()}.</i></p></div>
        </div>
      </div>
      <SummaryList />
      <footer className="footer">
        <p>&copy; {new Date().getFullYear()} | Sourced from HackerNews</p>
      </footer>
    </div>
  );
};

export default App;