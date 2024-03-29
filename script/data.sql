CREATE VIEW v_loan_church AS (
    SELECT
        l.id [id], 
        l.believer_id [believer_id],
        l.amount [amount],
        l.request_date [request_date],
        l.delivery_date [delivery_date],
        l.repay_date [repay_date],
        b.church_id [church_id]
    FROM Loan l
    JOIN believer b ON b.id = l.believer_id
);

INSERT INTO [church_group] (name) VALUES
    ('Group 1');

INSERT INTO [church] ([name], [church_group_id]) VALUES
    ('Church 1', 'CHG0001'),
    ('Church 2', 'CHG0001');

INSERT INTO [believer] ([name], [first_name], [password], [integration_date], [church_id]) VALUES
    ('Believer', '001', HASHBYTES('SHA2_256', 'pwd001'), CAST(GETDATE() AS DATE), 'CHU0001'),
    ('Believer', '002', HASHBYTES('SHA2_256', 'pwd002'), CAST(GETDATE() AS DATE), 'CHU0001'),
    ('Believer', '003', HASHBYTES('SHA2_256', 'pwd003'), CAST(GETDATE() AS DATE), 'CHU0001'),
    ('Believer', '004', HASHBYTES('SHA2_256', 'pwd004'), CAST(GETDATE() AS DATE), 'CHU0001'),
    ('Believer', '005', HASHBYTES('SHA2_256', 'pwd005'), CAST(GETDATE() AS DATE), 'CHU0001');

INSERT INTO [donation] ([church_id], [amount], [date], [sunday_id]) VALUES
    ('CHU0001', 90000, '2023-01-01', 1), 
    ('CHU0001', 90000, '2023-01-08', 2),  
    ('CHU0001', 90000, '2023-01-15', 3), 
    ('CHU0001', 90000, '2023-01-22', 4),  
    ('CHU0001', 90000, '2023-01-29', 5),  
    ('CHU0001', 90000, '2023-02-05', 6), 
    ('CHU0001', 90000, '2023-02-12', 7),  
    ('CHU0001', 90000, '2023-02-19', 8),  
    ('CHU0001', 90000, '2023-02-26', 9),  
    ('CHU0001', 90000, '2023-03-05', 10), 
    ('CHU0001', 90000, '2023-03-12', 11), 
    ('CHU0001', 90000, '2023-03-19', 12),  
    ('CHU0001', 90000, '2023-03-26', 13), 
    ('CHU0001', 90000, '2023-04-02', 14),  
    ('CHU0001', 90000, '2023-04-09', 15),  
    ('CHU0001', 90000, '2023-04-16', 16), 
    ('CHU0001', 90000, '2023-04-23', 17), 
    ('CHU0001', 90000, '2023-04-30', 18),  
    ('CHU0001', 90000, '2023-05-07', 19),  
    ('CHU0001', 90000, '2023-05-14', 20),  
    ('CHU0001', 90000, '2023-05-21', 21),  
    ('CHU0001', 90000, '2023-05-28', 22),  
    ('CHU0001', 90000, '2023-06-04', 23),  
    ('CHU0001', 90000, '2023-06-11', 24),  
    ('CHU0001', 90000, '2023-06-18', 25),  
    ('CHU0001', 90000, '2023-06-25', 26),  
    ('CHU0001', 90000, '2023-07-02', 27),  
    ('CHU0001', 90000, '2023-07-09', 28), 
    ('CHU0001', 90000, '2023-07-16', 29),  
    ('CHU0001', 90000, '2023-07-23', 30), 
    ('CHU0001', 90000, '2023-07-30', 31), 
    ('CHU0001', 90000, '2023-08-06', 32), 
    ('CHU0001', 90000, '2023-08-13', 33),  
    ('CHU0001', 90000, '2023-08-20', 34),  
    ('CHU0001', 90000, '2023-08-27', 35),  
    ('CHU0001', 90000, '2023-09-03', 36),  
    ('CHU0001', 90000, '2023-09-10', 37),  
    ('CHU0001', 90000, '2023-09-17', 38),  
    ('CHU0001', 90000, '2023-09-24', 39),  
    ('CHU0001', 90000, '2023-10-01', 40),  
    ('CHU0001', 90000, '2023-10-08', 41),  
    ('CHU0001', 90000, '2023-10-15', 42),  
    ('CHU0001', 90000, '2023-10-22', 43),  
    ('CHU0001', 90000, '2023-10-29', 44),  
    ('CHU0001', 90000, '2023-11-05', 45),
    ('CHU0001', 90000, '2023-11-12', 46),  
    ('CHU0001', 90000, '2023-11-19', 47),  
    ('CHU0001', 90000, '2023-11-26', 48), 
    ('CHU0001', 90000, '2023-12-03', 49),  
    ('CHU0001', 90000, '2023-12-10', 50),  
    ('CHU0001', 90000, '2023-12-17', 51),  
    ('CHU0001', 90000, '2023-12-24', 52); 

INSERT INTO [donation] ([church_id], [amount], [date], [sunday_id]) VALUES
    ('CHU0001', 99000, '2024-01-07', 1), 
    ('CHU0001', 99000, '2024-01-14', 2),  
    ('CHU0001', 99000, '2024-01-21', 3),  
    ('CHU0001', 99000, '2024-01-28', 4),  
    ('CHU0001', 99000, '2024-02-04', 5),  
    ('CHU0001', 99000, '2024-02-11', 6),  
    ('CHU0001', 99000, '2024-02-18', 7), 
    ('CHU0001', 99000, '2024-02-25', 8),  
    ('CHU0001', 99000, '2024-03-03', 9); 
