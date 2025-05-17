
# Working Worktree
The working directory holds all works in progress. The server does not access this directory when in production mode.
changes made through the browser interface should ensure that each project branch only contains changes related to the
corresponding project directory. With the main branch always being checked out in the publish branch you should feel
secure that none of your work will be served to the client until you are ready to publish and merge them into main.
