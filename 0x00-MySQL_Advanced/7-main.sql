-- Show current users and corrections
SELECT * FROM users;
SELECT * FROM corrections;

SELECT "--";

-- Call the procedure for user Jeanne
CALL ComputeAverageScoreForUser((SELECT id FROM users WHERE name = "Jeanne"));

SELECT "--";

-- Show updated users table
SELECT * FROM users;
