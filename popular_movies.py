def sample_api_call_func(self):
        url = "https://imdb236.p.rapidapi.com/api/imdb/most-popular-movies"
        headers = {
    'x-rapidapi-key': "f8399543c8mshd81c73f23b85a74p139359jsn594071b0464f",
    'x-rapidapi-host': "imdb236.p.rapidapi.com"
}


        response = self.api_handler("GET", url, headers=headers, timeout=10)

        tv_shows = response
        if not tv_shows:
            raise APIDataError("No Movies found in API response")

        concise_show_list = []
        for show in tv_shows[:10]:
            image=show.get("primaryImage", "No Image available")
            title = show.get("primaryTitle", "Unknown Title")
            description = show.get("description", "No description available.")
            genres = ", ".join(show.get("genres", []))
            rating = show.get("averageRating", "N/A")
            url = show.get("url", "N/A")
            languages = ", ".join(show.get("spokenLanguages", []))

            show_summary = (
                f"📝 {description}\n"
                f"🎭 Genres: {genres}\n"
                f"⭐ IMDb Rating: {rating}\n"
                f"🗣️ Languages: {languages}\n"
                f"🔗 URL: {url}"
            )
            
            concise_show_list.append({
                "thumbnail": {
                    "image": image
                },
                "title": title,
                "description": show_summary,
                "actionables": [
                {
                    "actionable_text": "Select",
                    "location_required": False,
                    "is_default": 0,
                    "uri": "",
                    "type": "TEXT_ONLY",
                    "payload": {
                    "title": "Button  1",
                    "url": "",
                    "message": f"{title}",
                    "gogo_message": ""
                    }
                }
                ]
            })

        self.generate_hsl(concise_show_list)

    def generate_hsl(self, items):
        hsl = {
            "type": "CAROUSEL",
            "data": {
                "image_aspect_ratio": "1",
                "width": "MEDIUM",
                "items": items
            },
            "isNew": False
        }
        self.bot_responses = [hsl]
        return self.bot_responses
