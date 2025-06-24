def sample_api_call_func(self):
        genre = self.parameters.get("genre")



        url = "https://imdb236.p.rapidapi.com/api/imdb/search"
        querystring = {
            "type": "movie",
            "genre": genre,
            "rows": "25",
            "sortOrder": "ASC",
            "sortField": "id"
        }

        headers = {
            "x-rapidapi-key": "f8399543c8mshd81c73f23b85a74p139359jsn594071b0464f",
            "x-rapidapi-host": "imdb236.p.rapidapi.com"
        }

        response = self.api_handler("GET", url, headers=headers, params=querystring, timeout=10)

        movies = response.get("results") or []
        if not movies:
            raise APIDataError(f"No movies found for genre: {genre}")

        concise_movie_list = []
        for movie in movies[:10]:
            image = movie.get("primaryImage", "No Image available")
            title = movie.get("primaryTitle", "Unknown Title")
            description = movie.get("description", "No description available.")
            rating = movie.get("averageRating", "N/A")
            movie_url = movie.get("url", "N/A")
            genres = ", ".join(movie.get("genres") or [])
            languages = ", ".join(movie.get("spokenLanguages") or [])

            summary = (
                f"📝 {description}\n"
                f"🎭 Genres: {genres}\n"
                f"⭐ IMDb Rating: {rating}\n"
                f"🗣️ Languages: {languages}\n"
                f"🔗 URL: {movie_url}"
            )

            concise_movie_list.append({
                "thumbnail": {
                    "image": image
                },
                "title": title,
                "description": summary,
                "actionables": [
                    {
                        "actionable_text": "Select",
                        "location_required": False,
                        "is_default": 0,
                        "uri": "",
                        "type": "TEXT_ONLY",
                        "payload": {
                            "title": "Button 1",
                            "url": "",
                            "message": title,
                            "gogo_message": ""
                        }
                    }
                ]
            })

        self.generate_hsl(concise_movie_list)

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
