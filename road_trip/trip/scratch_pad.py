import pickle
import json
# from road_trip.trip.models import Trip

def w(data):
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))


def p():
    return pickle.load(open('data.pkl', 'rb'))


def main():
    data = p()
    # trip = Trip.objects.get(pk=3)
    w(
        [
            {
                "location": ", ".join(data[x][1]["city"]),
                "location_plus": ",+".join(data[x][1]["city"]),
                "stopover": False

            }

            for x in range(len(data))
        ]
    )

if __name__ == '__main__':
    main()
