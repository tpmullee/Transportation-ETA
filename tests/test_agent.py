import unittest
from agent import TransportationAgentAI
from visualizations import plot_route
import pandas as pd
import os

class TestTransportationAgent(unittest.TestCase):
    """
    Unit tests for the TransportationAgentAI class.
    """

    def setUp(self):
        """
        Set up a TransportationAgentAI instance and mock data for testing.
        """
        self.agent = TransportationAgentAI()
        self.mock_data = pd.DataFrame({
            "distance_km": [100, 200, 300],
            "weather_factor": [1.0, 1.2, 0.8],
            "traffic_factor": [1.0, 1.1, 0.9],
            "delay_minutes": [10, 20, 30],
        })
        self.agent.train_model(self.mock_data)

    def test_add_route(self):
        """
        Test adding a route to the agent.
        """
        self.agent.add_route("R1", "Chicago", "Detroit", 450)
        self.assertIn("R1", self.agent.routes)
        self.assertEqual(self.agent.routes["R1"]["start"], "Chicago")
        self.assertEqual(self.agent.routes["R1"]["distance_km"], 450)

    def test_predict_delays_valid_route(self):
        """
        Test delay prediction for a valid route.
        """
        self.agent.add_route("R1", "Chicago", "Detroit", 450)
        delay = self.agent.predict_delays("R1", weather_factor=1.2, traffic_factor=1.1)
        self.assertIsNotNone(delay)

    def test_predict_delays_invalid_route(self):
        """
        Test delay prediction for an invalid route.
        """
        with self.assertRaises(ValueError):
            self.agent.predict_delays("INVALID")

    def test_zero_distance_route(self):
        """
        Test adding and predicting delays for a route with zero distance.
        """
        self.agent.add_route("R2", "Chicago", "Chicago", 0)
        delay = self.agent.predict_delays("R2")
        self.assertEqual(delay.total_seconds(), 0)

    def test_extreme_factors(self):
        """
        Test delay prediction with extreme weather and traffic factors.
        """
        self.agent.add_route("R3", "Chicago", "Detroit", 450)
        delay = self.agent.predict_delays("R3", weather_factor=10.0, traffic_factor=10.0)
        self.assertGreater(delay.total_seconds(), 0)

    def test_model_training(self):
        """
        Test that the model is trained correctly and produces a valid R^2 score.
        """
        score = self.agent.model.score(self.mock_data[self.agent.features], self.mock_data["delay_minutes"])
        self.assertGreater(score, 0)

    def test_visualization(self):
        """
        Test route visualization using Folium.
        """
        self.agent.add_route("R1", "Chicago", "Detroit", 450)
        plot_route(
            route_id="R1",
            start=(41.8781, -87.6298),  # Chicago coordinates
            end=(42.3314, -83.0458),    # Detroit coordinates
            route_name="Chicago to Detroit"
        )
        self.assertTrue(os.path.exists("route_R1.html"))
        # Clean up after the test
        os.remove("route_R1.html")

if __name__ == "__main__":
    unittest.main()
