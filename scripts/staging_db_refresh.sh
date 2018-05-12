#!/bin/bash
echo "Refreshing Migrations"
./scripts/db.sh migrate:refresh
echo "Seeding Event Types"
./scripts/db.sh db:seed --seeder event_types_table_seeder
echo "Seeding Drinkers"
./scripts/db.sh db:seed --seeder drinkers_table_seeder
echo "Seeding Events for Every Drinker"
./scripts/db.sh db:seed --seeder events_table_seeder