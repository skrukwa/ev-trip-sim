"""TODO"""
from classes import _Edge
import googlemaps


def mutate_edges(edges: list[_Edge], gmaps: googlemaps.client.Client) -> list[_Edge]:
    """Takes a list of incomplete edges and returns a new list of edges completed by making calls
    to the given googlemaps client. Any failed calls will result in the edge being discarded.

    Note that normally, there are no failed calls.

    Prints a verbose summary.

    Preconditions:
        - all(edge.road_distance is None for edge in edges)
        - all(edge.time is None for edge in edges)
    """
    if input(f'you are about to make {len(edges)} calls to the provided client (Y/N)') == 'Y':
        result = []
        for edge in edges:
            if _mutate_edge(edge, gmaps):
                result.append(edge)

        print(f'successfully completed {len(result)}/{len(edges)} edges')
        return result
    else:
        raise KeyboardInterrupt


def _mutate_edge(edge: _Edge, gmaps: googlemaps.client.Client) -> bool:
    """Takes an incomplete edge and completes it by making a call to the given googlemaps client.

    Returns True if successful and mutated, or False if unsuccessful and no mutations made.

    This is a mutating method.

    Preconditions:
        - edge.road_distance is None
        - edge.time is None
    """
    endpoints_iter = iter(edge.endpoints)
    p1 = next(endpoints_iter).coord
    p2 = next(endpoints_iter).coord

    try:
        response = gmaps.directions(p1, p2)
    except Exception:
        return False

    road_distance = response[0]['legs'][0]['distance']['value'] / 1000
    time = response[0]['legs'][0]['duration']['value']
    edge.road_distance = road_distance
    edge.time = time

    return True