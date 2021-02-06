class queries:
    get_users_teams_userID = '''
        SELECT
            Teams.TeamID,
            Teams.Name,
            Teams.Description,
            Users.Username AS TeamOwner
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
            Teams.Description,
            Owner.UserName
        FROM Teams
            INNER JOIN Users AS Owner ON Owner.UserID = Teams.OwnerID
        WHERE Teams.TeamID = ?
        '''

    get_team_members_teamID = '''
        SELECT
            Users.UserID,
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

    get_project_projectID = '''
        SELECT
            p.ProjectID,
            p.Project,
            p.Description,
            p.TeamID,
            t.OwnerID
        FROM Projects AS p
        INNER JOIN Teams AS t ON t.TeamID = p.TeamID
        WHERE ProjectID = ?
        '''

    get_user_owned_projects = '''
        SELECT
            p.ProjectiD,
            p.Project,
            t.Name AS TeamName
        FROM Projects AS p
        INNER JOIN Teams AS t on t.TeamID = p.TeamID
        WHERE t.OwnerID = ?
        ORDER BY p.Project, p.ProjectID
    '''

    get_user_involved_projects = '''
        SELECT
            p.ProjectID,
            p.Project,
            t.Name AS TeamName
        FROM Projects AS p
            INNER JOIN projectUsers AS pu ON pu.ProjectiD = p.ProjectID
            INNER JOIN Teams AS t ON t.TeamID = p.TeamID
        WHERE pu.userID = ?
        AND pu.userID <> t.ownerID
        ORDER BY p.Project, p.ProjectID
        '''

    get_projectMemberDetails_projectID = '''
        SELECT
            u.UserID,
            u.UserName,
            u.FirstName,
            u.LastName,
            CASE
                WHEN u.UserID = t.OwnerID THEN 1
                ELSE 0
            END as IsOwner
        FROM ProjectUsers AS pu
            INNER JOIN Projects AS p on p.projectID = pu.projectID
            INNER JOIN Users as u on u.userID = pu.userID
            INNER JOIN Teams as t ON t.TeamID = p.TeamID
        WHERE pu.ProjectID = ?'''

    get_projectMembers_projectID = '''
        SELECT
            u.UserID
        FROM ProjectUsers AS pu
        INNER JOIN Users AS u ON u.UserID = pu.UserID
        WHERE pu.ProjectID = ?'''

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

    get_project_tasks = '''SELECT * FROM Tasks WHERE ProjectID = ? ORDER BY CreatedOn '''

    get_task_info = '''SELECT * FROM Tasks WHERE TaskID = ?'''

    get_task_history = '''
        SELECT
            th.TaskID,
            th.ModifiedDate,
            th.ChangeType,
            th.OldText,
            th.NewText,
            u.UserID,
            u.UserName,
            u.FirstName,
            u.LastName
        FROM TaskHistory AS th
            INNER JOIN Users AS u ON u.UserID = th.ChangedBy
        WHERE TaskID = ?
        ORDER BY ModifiedDate DESC'''

    get_task_comments = '''
        SELECT
            c.CommentID,
            c.CommentText,
            c.CommentedBy,
            c.CreatedOn,
            u.UserName,
            u.FirstName,
            u.LastName
        FROM Comments AS c
            INNER JOIN Users AS u ON u.UserID = c.CommentedBy
        WHERE TaskID = ?
        ORDER BY CreatedOn DESC
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

    add_project = '''
        INSERT INTO Projects
            (Project, Description, TeamID)
        VALUES(?, ?, ?)'''

    add_projectUsers = '''
        INSERT OR IGNORE INTO ProjectUsers
            (ProjectID, UserID)
        VALUES(?, ?)'''

    add_task = '''
        INSERT INTO Tasks
            (Task, CreatedBy, ProjectID)
        VALUES(?, ?, ?)
        '''

    add_task_comment = '''
        INSERT INTO Comments
            (CommentText, CommentedBy, TaskID)
        VALUES(?, ?, ?)
        '''

    toggle_task_completion_ID = '''
        UPDATE TASKS
        SET IsCompleted = CASE IsCompleted WHEN 1 THEN 0 ELSE 1 END
        WHERE TaskID = ?
        '''

    add_taskhistory = '''
        INSERT INTO TaskHistory
            (TaskID, ChangeType, ChangedBy, OldText, NewText)
        VALUES (?, ?, ?, ?, ?)
        '''

    delete_project = '''
        DELETE FROM Projects
        WHERE ProjectID = ?
        '''

    delete_task = '''
        DELETE FROM Tasks
        WHERE TaskID = ?
        '''

    clear_projectUsers = '''
        DELETE FROM ProjectUsers
        WHERE ProjectID = ?'''

    update_project = '''
        UPDATE Projects
        SET Project = ?,
            Description = ?
        WHERE ProjectID = ?'''

    update_task = '''
        UPDATE Tasks
        SET Task = ?
        WHERE TaskID = ?
        '''
