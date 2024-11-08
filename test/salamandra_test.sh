curl --header "Content-Type: application/json" \
  	 --request GET \
     --data "`cat ./salamandra_test.json`" \
    127.0.0.1:8000/prompt_salamandra/