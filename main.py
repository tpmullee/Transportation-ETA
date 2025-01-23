import argparse
from agent import TransportationAgentAI

# Initialize the TransportationAgentAI
agent = TransportationAgentAI()

def add_route(args):
    """
    Add a new route to the agent.
    """
    agent.add_route(args.route_id, args.start, args.end, args.distance)
    print(f"Route {args.route_id} added: {args.start} -> {args.end} ({args.distance} km)")

def predict_delay(args):
    """
    Predict delays for a specific route.
    """
    try:
        new_eta = agent.predict_delays(args.route_id, args.weather, args.traffic)
        print(f"Predicted ETA with delays for route {args.route_id}: {new_eta}")
    except ValueError as e:
        print(f"Error: {e}")

def visualize_route(args):
    """
    Visualize a route on a map using Folium.
    """
    from visualizations import plot_route
    route = agent.routes.get(args.route_id)
    if not route:
        print(f"Error: Route {args.route_id} not found.")
        return
    plot_route(
        route_id=args.route_id,
        start=(41.8781, -87.6298),  # Example: Chicago coordinates
        end=(42.3314, -83.0458),    # Example: Detroit coordinates
        route_name=f"{route['start']} to {route['end']}"
    )
    print(f"Route {args.route_id} visualization saved as route_{args.route_id}.html.")

# Set up CLI commands using argparse
def main():
    parser = argparse.ArgumentParser(description="Transportation ETA CLI Tool")
    subparsers = parser.add_subparsers()

    # Add Route Command
    parser_add = subparsers.add_parser("add_route", help="Add a new route.")
    parser_add.add_argument("--route_id", required=True, help="Unique route ID.")
    parser_add.add_argument("--start", required=True, help="Starting location.")
    parser_add.add_argument("--end", required=True, help="Ending location.")
    parser_add.add_argument("--distance", required=True, type=float, help="Distance in kilometers.")
    parser_add.set_defaults(func=add_route)

    # Predict Delay Command
    parser_predict = subparsers.add_parser("predict", help="Predict delays for a route.")
    parser_predict.add_argument("--route_id", required=True, help="Route ID.")
    parser_predict.add_argument("--weather", type=float, default=1.0, help="Weather factor (default: 1.0).")
    parser_predict.add_argument("--traffic", type=float, default=1.0, help="Traffic factor (default: 1.0).")
    parser_predict.set_defaults(func=predict_delay)

    # Visualize Route Command
    parser_visualize = subparsers.add_parser("visualize", help="Visualize a route.")
    parser_visualize.add_argument("--route_id", required=True, help="Route ID.")
    parser_visualize.set_defaults(func=visualize_route)

    # Parse arguments and execute commands
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

