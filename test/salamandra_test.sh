curl --header "Content-Type: application/json" \
  	 --request GET \
     --data '{
		"system_prompt": "You are an eloquent, funny and whimsical assistant.",
		"prompt": "I need help! Send me a good book recommendation!"
	}' \
    127.0.0.1:8000/prompt_salamandra/