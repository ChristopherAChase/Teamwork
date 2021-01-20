SELECT * FROM Users;


CREATE TABLE Users(
    UserID      INTEGER         PRIMARY KEY AUTOINCREMENT,
    UserName    TEXT    UNIQUE  NOT NULL,
    Password    TEXT            NOT NULL,
    Email       TEXT    UNIQUE  NOT NULL,
    FirstName   TEXT            NOT NULL,
    LastName    TEXT            NOT NULL
);

CREATE TABLE Teams (
    TeamID      INTEGER     PRIMARY KEY AUTOINCREMENT,
    Name        TEXT        NOT NULL,
    OwnerID     INTEGER     NOT NULL,
    CreatedOn   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Description TEXT        NOT NULL DEFAULT 'New Team',
    UNIQUE(Name, OwnerID),
    FOREIGN KEY (OwnerID) REFERENCES Users (UserID)
);

CREATE TABLE Projects (
    ProjectID   INTEGER     PRIMARY KEY AUTOINCREMENT,
    Project     TEXT        NOT NULL,
    Description TEXT        NOT NULL DEFAULT 'New project',
    CreatedOn   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TeamID      INTEGER     NOT NULL,
    FOREIGN KEY (TeamID) REFERENCES Teams (TeamID)
);

CREATE TABLE Tasks (
    TaskID      INTEGER     PRIMARY KEY AUTOINCREMENT,
    Task        TEXT        NOT NULL,
    CreatedOn   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CreatedBy   INTEGER     NOT NULL,
    IsCompleted INTEGER     NOT NULL DEFAULT 0,
    ProjectID   INTEGER     NOT NULL,
    FOREIGN KEY (CreatedBy) REFERENCES Users (UserID),
    FOREIGN KEY (ProjectID) REFERENCES Projects (ProjectID),
    CHECK (isCompleted == 0 or isCompleted == 1)
);

CREATE TABLE Comments (
    CommentID   INTEGER     PRIMARY KEY AUTOINCREMENT,
    CommentText TEXT        NOT NULL,
    CommentedBy INTEGER     NOT NULL,
    CreatedOn   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TaskID      INTEGER     NOT NULL,
    FOREIGN KEY (CommentedBy) REFERENCES Users (UserID)
    FOREIGN KEY (TaskID) REFERENCES Tasks (TaskID)
);

CREATE TABLE UserTeams (
    UserTeamID  INTEGER     PRIMARY KEY AUTOINCREMENT,
    UserID      INTEGER     NOT NULL,
    TeamID      INTEGER     NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (TeamID) REFERENCES Teams (TeamID)
);


CREATE TABLE TaskHistory (
    TaskID          INTEGER     NOT NULL,
    ModifiedDate    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ChangeType      TEXT        NOT NULL,
    ChangedBy       INTEGER     NOT NULL,
    OldText         TEXT        NOT NULL,
    NewText         TEXT        NOT NULL,
    FOREIGN KEY (TaskID) REFERENCES Tasks (TaskID),
    FOREIGN KEY (ChangedBy) REFERENCES Users (UserID),
    PRIMARY KEY (TaskID, ModifiedDate),
    CHECK(ChangeType IN ('A', 'C', 'D', 'M'))
);

