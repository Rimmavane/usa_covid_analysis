#!/usr/bin/env bash

# BASIC STATISTICS
python scripts/cumulative_covid_cases_and_deaths_usa_states.py
python scripts/daily_covid_deaths_usa.py

# TAB US STATES
python scripts/map_cases.py -m 1;
python scripts/cases_deaths.py -m 1;
python scripts/cases_deaths_animation.py -m 1;
python scripts/tests_cases.py -m 1;

# TAB USA vs WORLD
python scripts/total_covid_cases_usa_vs_world.py
python scripts/new_covid_cases_per_day_usa_vs_world.py
python scripts/total_covid_deaths_usa_vs_world.py
python scripts/new_deaths_covid_per_day_usa_vs_world.py

# TAB EXTRAS
python scripts/death_causes_comparison_weekly_usa.py