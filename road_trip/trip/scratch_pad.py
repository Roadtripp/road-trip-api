import pickle
import json
# from models import Trip


def w(data):
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))


def p():
    return pickle.load(open('data.pkl', 'rb'))


def main():
    data = p()
    # trip = Trip.objects.get(pk=3)
    data = [{"all_activities": city} for city in data]
    c = ["activity", "food", "sports", "artist", "hotel"]
    for city in data:
        for category in c:
            city[category] = []
        for activity in city["all_activities"]:
            city[activity["category"]].append(activity)

    w(
        [
            {
                "location": ", ".join(x["all_activities"][1]["city"]),
                "location_plus": ",+".join(x["all_activities"][1]["city"]),
                "stopover": False,
                "activities": [
                    {
                        "title": item["name"],
                        "address": " ".join(item["address"]),
                        "sub_categories": item["subcategory"],
                        "activity_stopover": False,
                        "url": item["url"],
                        "small_rate_img_url": item["rating_img_url_small"],
                        "large_rate_img_url": item["rating_img_url"],
                        "average_rating": item["rating"],
                        "num_ratings": item["num_reviews"]


                    }
                    for item in x["activity"]
                ]

            }

            for x in data
        ]
    )


if __name__ == '__main__':
    main()
