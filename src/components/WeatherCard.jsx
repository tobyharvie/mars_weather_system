// components/WeatherCard.jsx
import React from 'react';
import '../style/WeatherCard.css'; 

const WeatherCard = ({ data, isHistoric, isToday, isForecast }) => {
  return (
    <div className={`weather-card ${isToday ? 'today' : ''}`}>
        {isHistoric && <p className="historic-label">Historic</p>}
        {isToday && <p className="today-label">Today</p>}
        {isForecast && <p className="forecast-label">Forecast</p>}
      <h2 className='sol-title'>Sol {data.sol}</h2>
      <p className="weather-data">{data.min_temp} | {data.max_temp} °C</p>
    </div>
  );
};

export default WeatherCard;