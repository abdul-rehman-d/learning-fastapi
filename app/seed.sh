#!/bin/bash

function get_body() {
	jq -n \
	--arg name "$1" \
	--arg secret_name "$2" \
	--argjson team_id "$3" \
	'{name: $name, secret_name: $secret_name, age: null, team_id: $team_id}'
}

function up() {
	justice=$(curl http://localhost:8000/teams \
		-H "Content-Type: application/json" \
		-d '{
		"name": "justice league",
		"headquarters": "hall of justice"
	}' | jq .id)

	teen=$(curl http://localhost:8000/teams \
		-H "Content-Type: application/json" \
		-d '{
		"name": "teen titans",
		"headquarters": "titans tower"
	}' | jq .id)

	body1=`get_body "batman" "bruce wayne" $justice`
	body2=`get_body "superman" "clark kent" $justice`
	body3=`get_body "nightwing" "dick grayson" $teen`
	body4=`get_body "starfire" "koriandr" $teen`

	curl http://localhost:8000/heroes \
		-H "Content-Type: application/json" \
		-d "$body1" | jq

	curl http://localhost:8000/heroes \
		-H "Content-Type: application/json" \
		-d "$body2" | jq

	curl http://localhost:8000/heroes \
		-H "Content-Type: application/json" \
		-d "$body3" | jq

	curl http://localhost:8000/heroes \
		-H "Content-Type: application/json" \
		-d "$body4" | jq
}

function down() {
	for id in $(curl -s http://localhost:8000/heroes | jq -r '.[].id'); do
		curl -X DELETE "http://localhost:8000/heroes/$id"
	done

	for id in $(curl -s http://localhost:8000/teams | jq -r '.[].id'); do
		curl -X DELETE "http://localhost:8000/teams/$id"
	done
}

case "$1" in
	up)
		echo "Running up..."
		up
		;;

	down)
		echo "Running down..."
		down
		;;

	*)
		echo "Usage: $0 [up|down]"
		exit 1
		;;
esac
