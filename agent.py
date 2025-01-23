import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import timedelta

class TransportationAgentAI:
    """
    A machine learning-powered agent for optimizing supply chain routes.
    Predicts delays and optimizes routes based on input factors.

    Attributes:
        name (str): Name of the agent.
        routes (dict): Dictionary of routes managed by the agent.
        model (LinearRegression): The machine learning model for delay prediction.
        features (list): List of input features for the model.
    """

    def __init__(self, name: str = "SupplyChainAI"):
        """
        Initializes the agent with a name and sets up internal data structures.

        Args:
            name (str): Name of the agent. Defaults to "SupplyChainAI".
        """
        self.name = name
        self.routes = {}
        self.model = None
        self.features = ["distance_km", "weather_factor", "traffic_factor"]

    def add_route(self, route_id: str, start_location: str, end_location: str, distance_km: float) -> None:
        """
        Adds a new route to the agent.

        Args:
            route_id (str): Unique identifier for the route.
            start_location (str): Starting location of the route.
            end_location (str): Ending location of the route.
            distance_km (float): Distance of the route in kilometers.
        """
        avg_speed_kmh = 60  # Default average speed
        estimated_time = timedelta(hours=distance_km / avg_speed_kmh)
        self.routes[route_id] = {
            "start": start_location,
            "end": end_location,
            "distance_km": distance_km,
            "estimated_time": estimated_time,
        }
        print(f"Route {route_id} added: {start_location} -> {end_location} ({distance_km} km)")

    def train_model(self, data: pd.DataFrame) -> None:
        """
        Trains a machine learning model using historical data.

        Args:
            data (pd.DataFrame): Historical data with features and delays.

        Raises:
            ValueError: If the data does not contain required columns.
        """
        if not all(feature in data.columns for feature in self.features + ["delay_minutes"]):
            raise ValueError("Data must include features and 'delay_minutes' column.")

        X = data[self.features]
        y = data["delay_minutes"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        # Evaluate the model
        score = self.model.score(X_test, y_test)
        print(f"Model trained with R^2 score: {score:.2f}")

    def predict_delays(self, route_id: str, weather_factor: float = 1.0, traffic_factor: float = 1.0) -> timedelta:
        """
        Predicts delays for a specific route using the trained machine learning model.

        Args:
            route_id (str): The ID of the route for which delays are to be predicted.
            weather_factor (float): Multiplier to account for weather conditions.
            traffic_factor (float): Multiplier to account for traffic conditions.

        Returns:
            timedelta: Predicted delay time.

        Raises:
            ValueError: If the route ID is not found or the model is not trained.
        """
        if route_id not in self.routes:
            raise ValueError(f"Route {route_id} not found.")

        if not self.model:
            raise ValueError("Model not trained. Please train the model with historical data first.")

        route = self.routes[route_id]

        # Handle zero distance explicitly
        if route["distance_km"] == 0:
            print(f"Route {route_id} has zero distance. No delay expected.")
            return timedelta(seconds=0)

        features = np.array([[route["distance_km"], weather_factor, traffic_factor]])
        predicted_delay_minutes = self.model.predict(features)[0]
        predicted_delay = timedelta(minutes=predicted_delay_minutes)
        new_eta = route["estimated_time"] + predicted_delay

        print(f"Predicted delay for route {route_id}: {predicted_delay}. New ETA: {new_eta}")
        return new_eta


    def optimize_routes(self):
        """
        Suggests optimized routes by reducing predicted delays by a predefined percentage.

        Returns:
            list[dict]: A list of dictionaries with original and optimized route times.
        """
        if not self.model:
            raise ValueError("Model not trained. Train the model with historical data first.")

        optimized_routes = []
        for route_id, details in self.routes.items():
            features = np.array([[details["distance_km"], 1.0, 1.0]])
            original_delay = timedelta(minutes=self.model.predict(features)[0])
            optimized_delay = original_delay * 0.9  # Assume a 10% optimization
            optimized_time = details["estimated_time"] + optimized_delay
            optimized_routes.append({
                "route_id": route_id,
                "original_time": details["estimated_time"] + original_delay,
                "optimized_time": optimized_time,
            })
        return optimized_routes

    def display_routes(self) -> None:
        """
        Displays all the routes currently managed by the agent.
        """
        for route_id, details in self.routes.items():
            print(f"Route {route_id}: {details['start']} -> {details['end']}, "
                  f"Distance: {details['distance_km']} km, "
                  f"Estimated Time: {details['estimated_time']}")
