class queries:
    get_users_teams_userID = '''
        SELECT
            Teams.Name,
            Teams.Description,
            Users.Username
        FROM Teams
        INNER JOIN UserTeams ON Teams.TeamID = UserTeams.TeamID
        INNER JOIN Users ON Users.UserID = Teams.OwnerID
        WHERE UserTeams.UserID = ?'''

    get_user_userID = 'SELECT * FROM Users WHERE UserID = ?'

    get_user_userName = 'SELECT * FROM Users WHERE UserName = ?'

    get_user_email = 'SELECT * FROM Users WHERE Email = ?'

    check_teams = 'SELECT * FROM Teams WHERE Name = ? and OwnerID = ?'

    add_user = '''
        INSERT INTO Users
            (Username, Password, Email, Firstname, LastName)
        VALUES (?, ?, ?, ?, ?)'''

    add_team = '''
        INSERT INTO Teams
            (Name, OwnerID, Description)
        VALUES (?,?,?)'''

    add_userTeam = '''
        INSERT INTO UserTeams
            (UserID, TeamID)
        VALUES(?,?)'''
