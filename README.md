<h1>Caregiving Management Platform</h1>

**Latest Update(s):** 
[May] Recommendation system implemented and tested.<br> 
[Apr] Initial commit of overdue local progress. Migrated from SQLite3 to PostgreSQL.<br>

**Developer Note:** Recommendation system is done. Just needs to a fluid integration with everything else.

<h3>PxostgreSQL Setup</h3>

```bash
brew install postgresql
brew services start postgresql
sudo -i -u postgres
psql -d postgres -f ./backend/functions/create_psql_admin.sql
\q
pip3 install psycopg2-binary
```

Recommendation system logic:
0. Initiate Process: Careseeker defines care requirements.
1. Data Collection: Retrieve and encode data to quantifiables.
2. Data Preprocessing: Normalize, standardize, and vectorize data.
3. Data Fitting: Transfer over to scikit-leaarn's KNN.
4. Similarity Searching: Apply same data transformations for careseeker requirements. 
5. Data Postprocessing: Apply additional data filtering (e.g., distance, pay rate, etc.).
