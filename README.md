<h1>Caregiving Management Platform</h1>

This is software designed for caregiving businesses to promote and manage their talents and services.<br>

**Latest Update(s):** Initial commit of overdue local progress. Migrated from SQLite3 to PostgreSQL.<br>

**Developer Note:** This is my next big project, which I started in the beginning of March 2025. 
I've been working as a hospice caregiver fulltime and developing this app on the side. 
I'll be slowly rolling out features/updates and hopefully a working version of the site for caregivers and clients to use. 
The expect release of a working version is around early May 2025. 
I'm also down developer power. So, if anyone wants to join in, please let me know.

<h3>PxostgreSQL Setup</h3>

```bash
brew install postgresql
brew services start postgresql
sudo -i -u postgres
psql -d postgres -f ./backend/functions/create_psql_admin.sql
\q
pip3 install psycopg2-binary
brew install postgis
brew services restart postgresql
```

Recommendation system logic:
[0] Quantify caregiver qualifications.
[1] Retrieve caregivers within n-miles of the area.
[2] Compute scores from applicable qualifications.
[3] Sort by highest summed qualification value values.

[1] Distance calculation:
Relevant methods:
CrudFunctions.retrieve_caregivers_within_n_distance()

Use Haversine distance calculation for near-accurate
approximations.

[2] Scoring:
Relevant methods:
QuantifyUserData.score_caregiver_qualifications_on_careseeker_requirements()

Quantification of qualifications: Both values must be 
True to count as there is no need to give score to a
qualification that a seeker does not require of.

Example:
Seeker Requirements:  [0, 1, 0, 0, 1, 1]
Giver Qualifications: [1, 0, 0, 0, 1, 1]
Qualifications Met:   [0, 1, 0, 0, 1, 1]
Score:                2/3 = 66.66% = 0.6666...

Quantification of non-qualifications: Non-qualifications
will be based on how beneficial they are to the seeker. 
This quantification is mostly for non 0/1 values, but
rather for values that can range arbitrarily.

Example:
nth_user_yoe_score = years_of_experience / sum_of_all_years_of_experience
nth_user_yoe_score = 9 / (3 + 2 + 11 + ... + 7) 
                    = 9 / (100)
                    = 9%
                    = 0.09

nth_user_distance_score = (sum_of_all_distances - distance_from_seeker) / sum_of_all_distances
nth_user_distance_score = 13 / (4 + 5 + 25 + ... + 17)
                        = 13 / (1000)
                        = 1.3%
                        = 0.013

bonus_score = (score_1 * (1/num_of_scores)) + ... + (score_n * (1/num_of_scores))
bonus_score = (.09 * (1/2)) + (.013 * (1/2))
            = 0.045 + 0.0065
            = 0.0515

Final calculations: The bonus score should only contribute
up to an arbtrirarily and appropriately set fraction of the
qualifying score. Since the maximum qualification score is 1,
then the bonus score contribution should be: 0 < bonus_score < 1.

Example:
bonus_score_contribution_limit = 50% = 0.5
final_score = qualification_score + (bonus_score * bonus_score_contribution_limit)
            = 0.6666 + (0.0515 * 0.5)
            = 0.6666 + (0.02575)
            = 0.69235

Thus, the final score is 0.69235. This user will be a 69.235%
match to the seeker.

Note 1: Custom weights can be set for each bonus score rather
than having all scores weighed equally based on the number
of scores. Especially for values like years of experience
potentially needing to outweigh distance as a bonus score.

Note 2: The bonus score contribution limit value should be
tested qualitatively based on the recommendation results,
and should be adjusted accordingly if it's contributing too
much or not at all.
