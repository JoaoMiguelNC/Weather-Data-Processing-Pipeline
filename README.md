# Weather Data Processing Pipeline

Version `0.2.2`

## API

The API https://weather-api-724625757672.europe-west1.run.app can be used to get the current weather for a given city using `/weather/current/<location>` where `<location>` is the name of the city.

The API returns data for all cities with the name given, for a more precise result, use `city,country` or `city,state,country` where `country` is the ISO 3166 country code, and if `state` is the state code for cities in the US.