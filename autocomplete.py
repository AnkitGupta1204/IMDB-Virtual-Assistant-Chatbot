def sample_api_call_func(self):
        search_query = self.parameters.get("search_query", "break")
        url = f"https://imdb236.p.rapidapi.com/api/imdb/autocomplete?query={search_query}"

        headers = {
	"x-rapidapi-key": "f8399543c8mshd81c73f23b85a74p139359jsn594071b0464f",
	"x-rapidapi-host": "imdb236.p.rapidapi.com"
}


        response = self.api_handler("GET", url, headers=headers, timeout=10)

        tv_shows = response
        if not tv_shows:
            raise APIDataError("No Movies/ Shows found in API response")

        concise_show_list = []
        for show in tv_shows[:min(10, len(tv_shows))]:
            image=show.get("primaryImage", "No Image available")
            title = show.get("primaryTitle", "Unknown Title")
            description = show.get("description", "No description available.")
            rating = show.get("averageRating", "N/A")
            url = show.get("url", "N/A")
            genres = ", ".join(show.get("genres") or [])
            languages = ", ".join(show.get("spokenLanguages") or [])


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


    def api_handler(self, method, url, handle_error_status_code=None, **kwargs):
        """
        Performs API calls and handles logging + error management
        """
        try:
            request_start_time = time.time()
            logger.info(f"Calling {url} on behalf of function '{inspect.currentframe().f_back.f_code.co_name}'"
                        f" with payload: {kwargs.get('data') or kwargs.get('json')}")
            response = haptik_requests.request(method=method.lower(), url=url, **kwargs)
            logger.info(f"Took {time.time() - request_start_time} sec to call {url},"
                        f" got status code {response.status_code}")

            if response.status_code is None:
                logger.info(f"Unable to reach URL {url}")
                raise requests_og.exceptions.ConnectionError()
            elif response.ok:
                logger.info(f"[Success] url: {url} response: {response.text}")
                response = self.transform_to_dict(response.text)
                return response
            elif handle_error_status_code is not None:
                return handle_error_status_code(response)
            elif response.status_code == 408:
                raise requests_og.exceptions.Timeout()
            else:
                raise requests_og.exceptions.HTTPError()
        except requests_og.exceptions.Timeout as errt:
            logger.exception(f"[Error] {errt} url: {url}")
            raise
        except (requests_og.exceptions.ConnectionError, requests_og.exceptions.HTTPError) as errc:
            logger.exception(f"[Error] {errc} url: {url}")
            raise
        except Exception as err:
            logger.exception(f"[Error] {err} url: {url}")
            raise

    @staticmethod
    def transform_to_dict(data):
        try:
            return json.loads(data)
        except ValueError:
            try:
                return xmltodict.parse(re.sub(r'xmlns:[^>]*|nsd+:|SOAP:', '', data))
            except:
                return data

    def get_final_response(self, **kwargs):
        final_response = {
            **kwargs,
            **self.output_data,
            'conversation_details': self.conversation_details,
            'user_details': self.user_details
        }
        logger.info(f"final_response {final_response}")
        return {
            'statusCode': 200,
            'body': json.dumps(final_response),
            'headers': {'Content-Type': 'application/json'}
