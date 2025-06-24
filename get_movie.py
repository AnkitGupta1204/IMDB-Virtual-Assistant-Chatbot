def sample_api_call_func(self):
        imdb_id= self.parameters.get("imdb_id", "NA")
        url = f"https://imdb236.p.rapidapi.com/api/imdb/{imdb_id}"

        headers = {
	"x-rapidapi-key": "f8399543c8mshd81c73f23b85a74p139359jsn594071b0464f",
	"x-rapidapi-host": "imdb236.p.rapidapi.com"
}


        response = self.api_handler("GET", url, headers=headers, timeout=10)

        if not response:
            raise APIDataError("No Movies/ Shows found in API response")

        concise_show_list = []
        image=response.get("primaryImage", "No Image available")
        title = response.get("primaryTitle", "Unknown Title")
        description = response.get("description", "No description available.")
        genres = ", ".join(response.get("genres", []))
        rating = response.get("averageRating", "N/A")
        url = response.get("url", "N/A")
        languages = ", ".join(response.get("spokenLanguages", []))

        show_summary = (
                f"▶️ **{title}**\n"
                f"📝 {description}\n"
                f"🎭 Genres: {genres}\n"
                f"⭐ IMDb Rating: {rating}\n"
                f"🗣️ Languages: {languages}\n"
                f"🔗 URL: {url}"
            )
            
        concise_show_list.append(show_summary)
        self.bot_responses = concise_show_list
        return self.bot_responses
