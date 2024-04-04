import React, { useEffect, useState } from 'react';
import axios from 'axios';

const SummaryList = () => {
  const [summaries, setSummaries] = useState([]);

  useEffect(() => {
    const fetchSummaries = async () => {
      try {
        const response = await axios.get('/api/summaries/all');
        setSummaries(response.data);
      } catch (error) {
        console.error('Error fetching summaries:', error);
      }
    };

    fetchSummaries();
  }, []);

    // Sort summaries by date in descending order
    const sortedSummaries = summaries.sort((a, b) => new Date(b.date) - new Date(a.date));

    return (
    <div>
        <div className="content">
        {sortedSummaries.map((summary) => {
            // Format the date
            let date = new Date(summary.date);
            let formattedDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

            return (
            <div key={summary.id}>
                <h3>{formattedDate}</h3> {/* Use the formatted date here */}
                <p>{summary.summary}</p>
                <ul>
                {summary.links.map((link, index) => (
                    <li key={index}>
                    <a href={link} target="_blank" rel="noopener noreferrer">{link}</a>
                    </li>
                ))}
                </ul>
            </div>
            );
        })}
        </div>
    </div>
    );
}

export default SummaryList;