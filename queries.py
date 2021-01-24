class queries:
    get_users_teams_userID = '''
        SELECT
            Teams.TeamID,
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

    get_team_info = '''
        SELECT
            Teams.TeamID,
            Teams.Name,
            Teams.Description
        FROM Teams
        WHERE Teams.TeamID = ?
        '''

    get_team_members_teamID = '''
        SELECT
            Users.Username,
            Users.FirstName,
            Users.LastName,
            Users.Email,
            CASE
                WHEN Users.UserID = Teams.OwnerID THEN 1
                ELSE 0
            END AS IsOwner
        FROM Teams
        INNER JOIN UserTeams ON UserTeams.TeamID = Teams.TeamID
        INNER JOIN Users ON Users.UserID = userTeams.UserID
        WHERE Teams.TeamID = ?
        ORDER BY IsOwner DESC
        '''

    get_projects_teamID = '''
        SELECT
            Projects.ProjectID,
            Projects.Project,
            Projects.Description
        FROM Projects
        WHERE TeamID = ?
        '''

    get_teams_search = '''
        SELECT
            Teams.TeamID,
            Teams.Name,
            Teams.Description,
            Users.Username
        FROM Teams
        INNER JOIN Users ON Users.UserID = Teams.OwnerID
        WHERE Users.UserName LIKE ?
        OR Teams.Name LIKE ?
        '''

    check_teams = 'SELECT * FROM Teams WHERE Name = ? and OwnerID = ?'

    check_user_on_team = '''
        SELECT COUNT(*)
        FROM UserTeams
        WHERE UserID = ?
            AND TeamID = ?
        '''

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
