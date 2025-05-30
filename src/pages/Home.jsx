import { useState, useEffect } from "react";
import WeatherCard from "../components/WeatherCard";
import '../style/Home.css'; 
const NASAapiKey = "tXddYe5swgCJwwMxjVhOsYKx4bOhxBzV52cbUBOF";
const NASAapiUrl = 'https://api.nasa.gov/insight_weather/?api_key='+NASAapiKey+'&feedtype=json&ver=1.0';
const modelAPIPath = 'http://localhost:5000/api/forecast'

export default function Home() {

    const [weatherData, setWeatherData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [forecastData, setForecast] = useState(null);
    const [forecastLoading, setForecastLoading] = useState(true);
    const [forecastError, setForecastError] = useState(false);

    useEffect(() => {
        // get mars weather data from NASA API
        fetch(NASAapiUrl)
        .then(res => { return res.json()} )
        .then(data => {
            setWeatherData(data);
            setLoading(false);
            console.log('Weather data:', data)
        }).catch(err => {
            setError(true);
            setLoading(false);
        }); 
    }, []);

    useEffect(() => {
        if (loading || !weatherData) { return };

        // get forecast data from backend model
        fetch(modelAPIPath, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            //body: JSON.stringify({sol:680})
            body: JSON.stringify(weatherData)
        }).then(res => { return res.json()})
        .then(data => {
            setForecast(data)
            setForecastLoading(false);
            console.log('Forecast result:', data);
        }).catch(err => {
            setForecastError(true);
            setForecastLoading(false);
        });  

    }, [weatherData]); // dependency on weather Data

    if (loading || forecastLoading) return <p>Loading Mars weather...</p>;
    if (error || forecastError) return <p className="text-red-500">{error}</p>;

    const sols = weatherData.sol_keys
    // todays sol number
    const solNum = Number(sols[6])

    const refinedWeatherData = [
        {sol:String(solNum-3), min_temp:weatherData[solNum-3].AT.mn, max_temp:weatherData[solNum-3].AT.mx},
        {sol:String(solNum-2), min_temp:weatherData[solNum-2].AT.mn, max_temp:weatherData[solNum-2].AT.mx},
        {sol:String(solNum-1), min_temp:weatherData[solNum-1].AT.mn, max_temp:weatherData[solNum-1].AT.mx},
        {sol:String(solNum), min_temp:weatherData[solNum].AT.mn, max_temp:weatherData[solNum].AT.mx},
        {sol:String(solNum+1), min_temp:forecastData[0].min_temp, max_temp:forecastData[0].max_temp},
        {sol:String(solNum+2), min_temp:forecastData[0].min_temp, max_temp:forecastData[0].max_temp},
        {sol:String(solNum+3), min_temp:forecastData[0].min_temp, max_temp:forecastData[0].max_temp}
    ];

    // Round all temperature and pressure values afterward
    const roundedWeatherData = refinedWeatherData.map(entry => ({
    ...entry,
    min_temp: Math.round(entry.min_temp),
    max_temp: Math.round(entry.max_temp)
    }));


    return (
        <div>
            <h2 className='home-description'>Weather from the Elysium Planatia, Planet Mars.</h2>
            <div className="app-container">
                {roundedWeatherData.map((item, index) => (
                    <WeatherCard
                    key={index}
                    data={item}
                    isHistoric={index < 3}
                    isToday={index === 3}
                    isForecast={index > 3}
                    />
                ))}
            </div>
        </div>
    );
}

