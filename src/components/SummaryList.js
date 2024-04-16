import React, { useEffect, useState } from 'react';
import axios from 'axios';

const SummaryList = () => {
  const [summaries, setSummaries] = useState([]);

  useEffect(() => {
    const fetchSummaries = async () => {
      try {
        const response = await axios.get('https://ai-timelines-eni7imw2ma-uc.a.run.app/api/summaries/all');
        if (Array.isArray(response.data)) {
          setSummaries(response.data);
        } else {
          console.error('Fetched data is not an array:', response.data);
        }
      } catch (error) {
        console.error('Error fetching summaries:', error);
      }
    };

    fetchSummaries();
  }, []);

  // Sort summaries by date in descending order, ensuring summaries is an array before sorting
  const sortedSummaries = summaries.length > 0
    ? [...summaries].sort((a, b) => new Date(b.date) - new Date(a.date))
    : [];

    return (
      <div>
        <div className="content">
          {sortedSummaries.map((summary, index) => {
            // Format the date
            let date = new Date(summary.date);
            let formattedDate = date.toISOString().split('T')[0];
    
            return (
              <div key={`${summary.date}-${index}`}>
                <h3>{formattedDate}</h3>
                <p>{summary.summary}</p>
                {summary.links && (
                  <div>
                    <h4>Links:</h4>
                    <ul>
                      {summary.links.map((link, linkIndex) => (
                        <li key={`${summary.date}-${index}-${linkIndex}`}>
                          <a href={link} target="_blank" rel="noopener noreferrer">{link}</a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
}

export default SummaryList;
