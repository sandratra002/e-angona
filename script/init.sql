CREATE TABLE [church_group] (
    [id] nvarchar(10) PRIMARY KEY DEFAULT (N'CHG' + RIGHT(REPLICATE(N'0', 4) + CONVERT(nvarchar(10), NEXT VALUE FOR [church_group_sequence]), 4)),
    [name] VARCHAR(100)
);

CREATE TABLE [church] (
    [id] nvarchar(10) PRIMARY KEY DEFAULT (N'CHU' + RIGHT(REPLICATE(N'0', 4) + CONVERT(nvarchar(10), NEXT VALUE FOR [church_sequence]), 4)),
    [name] VARCHAR(100) NOT NULL,
    [church_group_id] nvarchar(10)
);

ALTER TABLE [church]
ADD CONSTRAINT [church_group_fk_check] FOREIGN KEY ([church_group_id])
REFERENCES [church_group]([id]) 
ON DELETE CASCADE;

CREATE TABLE [believer] (
    [id] nvarchar(10) PRIMARY KEY DEFAULT (N'BEL' + RIGHT(REPLICATE(N'0', 4) + CONVERT(nvarchar(10), NEXT VALUE FOR [believer_sequence]), 4)),
    [church_id] nvarchar(10),
    [name] VARCHAR(100) NOT NULL,
    [first_name] VARCHAR(100) NOT NULL,
    [password] VARCHAR(255) NOT NULL,
    [integration_date] DATE DEFAULT CAST(GETDATE() AS date)
);

ALTER TABLE [believer]
ADD CONSTRAINT [believer_church_fk_check] FOREIGN KEY ([church_id])
REFERENCES [church]([id])
ON DELETE CASCADE;

CREATE TABLE [loan] (
    [id] nvarchar(10) PRIMARY KEY DEFAULT (N'LOA' + RIGHT(REPLICATE(N'0', 4) + CONVERT(nvarchar(10), NEXT VALUE FOR [loan_sequence]), 4)),
    [believer_id] nvarchar(10),
    [request_date] DATE NOT NULL DEFAULT CAST(GETDATE() AS date),
    [delivery_date] DATE NOT NULL,
    [repay_date] DATE DEFAULT NULL,
    [amount] DECIMAL(10, 2),
    CHECK ([amount] > 0),
);

ALTER TABLE [loan]
ADD CONSTRAINT [loan_believer_fk_check] FOREIGN KEY ([believer_id])
REFERENCES [believer]([id])
ON DELETE CASCADE;

CREATE OR REPLACE VIEW v_loan_church AS (
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

CREATE TABLE [donation] (
    [id] nvarchar(10) PRIMARY KEY DEFAULT (N'DON' + RIGHT(REPLICATE(N'0', 4) + CONVERT(nvarchar(10), NEXT VALUE FOR [donation_sequence]), 4)),
    [church_id] nvarchar(10),
    [amount] DECIMAL(10, 2),
    CHECK ([amount] > 0),
    [date] DATE NOT NULL,
    [sunday_id] INT NOT NULL,
    [is_prediction] INT DEFAULT 0,
    CHECK ([is_prediction] = 0 OR [is_prediction] = 1)
);

ALTER TABLE [donation]
ADD CONSTRAINT [donation_church_fk_check] FOREIGN KEY ([church_id])
REFERENCES [church]([id])
ON DELETE CASCADE;

CREATE TABLE [fund] (
    [id] nvarchar(10) PRIMARY KEY DEFAULT (N'FUN' + RIGHT(REPLICATE(N'0', 4) + CONVERT(nvarchar(10), NEXT VALUE FOR [fund_sequence]), 4)),
    [church_id] nvarchar(10),
    [date] DATE NOT NULL,
    [amount] DECIMAL(10, 2),
    CHECK ([amount] > 0)
);

ALTER TABLE [fund]
ADD CONSTRAINT [fund_church_fk_check] FOREIGN KEY ([church_id])
REFERENCES [church]([id])
ON DELETE CASCADE;